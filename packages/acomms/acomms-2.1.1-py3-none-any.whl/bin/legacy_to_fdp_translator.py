#!/usr/bin/python3

from acomms import Micromodem, UnifiedLog, Message
from acomms.modem_connections import UdpConnection as ModemUdpConnection
from acomms.flexibledataprotocol import FDPacket, FDFrame
import argparse
import socket
from threading import Thread
from queue import Queue, Empty
from time import sleep
import logging

class UdpConnection(object):
    def __init__(self, receive_callback, remote_host, remote_port, local_host=None, local_port=None, timeout=0.1):
        self._incoming_line_buffer = ""

        self.receive_callback = receive_callback
        self.timeout = timeout
        self._remote_host = remote_host
        self._remote_port = remote_port

        if local_host is None:
            self._local_host = ""
        else:
            self._local_host = local_host

        if local_port is None:
            self._local_port = remote_port
        else:
            self._local_port = local_port

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.bind(('', self._local_port))
        self._socket.settimeout(0.1)

        self._thread = Thread(target=self._listen)
        self._thread.setDaemon(True)
        self._thread.start()

    def close(self):
        self._thread.stop()

    def _listen(self):
        while True:
            msg_lines = self.readlines()
            # If we get data, we are connected, so pass through to the parser
            if msg_lines:
                for line in msg_lines:
                    self.receive_callback(line)

    def readlines(self):
        """Returns a \n terminated line  Only returns complete lines (or None on timeout)"""
        try:
            rl = self._socket.recv(1024)
        except socket.timeout:
            return None

        if len(rl) == 0:
            return None

        rl = rl.decode('ascii')

        self._incoming_line_buffer += rl

        # Make sure we got a complete line.  (We always should with RECON.)
        if '\n' in self._incoming_line_buffer:
            # is there a newline at the end?
            lines = self._incoming_line_buffer.splitlines(True)
            # See if the last line has a newline at the end.
            if lines[-1][-1] != '\n':
                self._incoming_line_buffer = lines[-1]
                lines.pop()  # remove it from the list to passed on
            else:
                self._incoming_line_buffer = ''
            # return the list of complete lines
            return lines
        else:
            return None

    def write(self, data):
        if type(data) is str:
            data = data.encode('ascii')
        self._socket.sendto(data, (self._remote_host, self._remote_port))

class FdpTranslator(object):
    def __init__(self, remote_address, remote_port, local_port=None, modem_serial_port=None, modem_baud=19200,
                 modem_remote_address=None, modem_remote_port=4001, modem_local_port=4001):
        self.modem_rx_queue = Queue()
        self.modem = Micromodem()
        # Now that we have a good time, start a new log with a good timestamp.
        unified_log = UnifiedLog(console_log_level=logging.INFO)
        self.modem.unified_log = unified_log
        if modem_serial_port:
            self.modem.connect_serial(modem_serial_port, modem_baud)
        else:
            self.modem.connection = ModemUdpConnection(self.modem, modem_remote_address,
                                                       modem_remote_port, local_port=modem_local_port)
        self.modem.attach_incoming_msg_queue(self.modem_rx_queue)

        self.udp_connection = UdpConnection(self.udp_receive_callback, remote_address, remote_port, local_port=local_port)

        self.modem_rx_thread = Thread(target=self.modem_receive_callback, daemon=True)
        self.modem_rx_thread.start()

    def modem_receive_callback(self):
        while True:
            try:
                message = self.modem_rx_queue.get(timeout=0.1)
                # Pass all messages through
                self.udp_connection.write(message['raw'].encode('ascii'))
                print("modem> {}".format(message["raw"].strip()))
                # CARFP messages will be handled by the modem directly
                # CAACK:
                if message['type'] == "CACDR":
                    # $CACDR,isodate,rxseqnum,src,dest,minirate,miniframe_ACK,dataframe_ACK,reserved1,…reserved6*CS
                    if int(message['params'][6]) > 0:
                        caack_msg = "$CAACK,{src},{dest},{frame_num},1\r\n".format(src=message['params'][2],
                                                                                   dest=message['params'][3],
                                                                                   frame_num=1)
                        self.udp_connection.write(caack_msg.encode('ascii'))
            except Empty:
                pass


    def udp_receive_callback(self, line):
        try:
            # Drop certain messages
            if line.startswith("$CCCYC"):
                cyc_msg = Message(line)
                self.udp_connection.write("$CACYC,{},{},{},{},{},{}\r\n".format(*cyc_msg['params']))
                self.udp_connection.write("$CADRQ,000000,{},{},0,32,1\r\n".format(cyc_msg['params'][1],
                                                                              cyc_msg['params'][2]))
            elif line.startswith("$CCTXD"):
                # turn this into a CCTFP message with ACK set
                txd_msg = Message(line) # $CCTXD,src,dest,ack,hexdata
                cctfp_msg = "$CCTFP,{dest},1,1,1,0,,{hexdata}".format(dest=txd_msg['params'][1],
                                                                      hexdata=txd_msg['params'][3])
                self.modem.write_nmea(cctfp_msg)
                print("modem< {}".format(cctfp_msg))
            # just pass through other messages
            else:
                self.modem.write_nmea(line)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='Connect to a MM for testing purposes')
    ap.add_argument("-C", "--COM", help='COM Port to connect', default="/dev/ttyO1")
    ap.add_argument("-BR", "--Baudrate", help="COM Port Baud Rate", default=19200)

    args = ap.parse_args()

    #translator = FdpTranslator("COM20", 19200, '10.11.62.211', 4001)
    translator = FdpTranslator(remote_address='10.19.30.199', remote_port=4002, local_port=4002,
                               modem_remote_address='10.19.30.61', modem_remote_port=4001, modem_local_port=4001)

    try:
        while True:
            sleep(1)
    finally:
        translator = None