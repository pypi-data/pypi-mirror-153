from acomms import Micromodem
from acomms.flexibledataprotocol import FDPacket, FDFrame

from acomms.net_packet import NetPacket

class NetModem(Micromodem):
    """Network enabled micromodem driver implementation"""

    def __init__(self, name='netmodem', unified_log=None,
                 log_path=None, log_level='INFO', sound_speed=1500, max_range_m = 5000):
        super(NetModem, self).__init__(name=name, unified_log=unified_log,
                                       log_path=log_path, log_level=log_level)

        # Use sound speed for calculating ranges and timeouts
        self.packet_timeout = max_range_m/sound_speed

        # Keep track of active links by the destination SRC ID
        # self.link_manager = LinkManager()

        # Acoustic networking is implemented on top of micromodem
        # Flexible data packets
        self.fdp_listeners.append(self.on_fdp_receive)

        # Different network protocols have their own handlers
        self.protocol_handlers = {}
        self.protocol_queues = {}

    def register_protocol_queue(self, pid, queue):
        self.protocol_queues.setdefault(pid, []).append(queue)

    def register_protocol_handler(self, pid, handler_func):
        self.protocol_handlers.setdefault(pid, []).append(handler_func)

    def on_fdp_receive(self, fdpacket):
        netpacket = NetPacket.from_fdpacket(fdpacket)

        callbackset = set()
        queueset = set()

        # Check each of the subheaders in the packet
        for key in netpacket.subheaders:
            subheader = netpacket.subheaders[key]
            pid = subheader[0]

            # For each PID with a registered handler, pass handler
            # the subheader and the netpacket
            if pid in self.protocol_handlers:
                for func in self.protocol_handlers[pid]:
                    callbackset.add(func)

            # For each PID with a registered queue, put
            # the netpacket on the queue
            if pid in self.protocol_queues:
                for queue in self.protocol_queues[pid]:
                    queueset.add(queue)

        # Callback all the functions in the set
        for func in callbackset:
            try:
                func(netpacket)
            except Exception as e:
                self._daemon_log.warn("Error with PID handler function: " + str(func) + " " + str(e))

        # Append netpacket to all queues in set
        for queue in queueset:
            try:
                queue.put_nowait(netpacket)
            except:
                self._daemon_log.warn("Error appending netpacket to protocol queue")

    def transmit_netpacket(self, netpacket, miniframerate, dataframerate, ack):
        self.send_fdpacket(netpacket.to_fdpacket(miniframerate=miniframerate,
                                                 dataframerate=dataframerate,
                                                 ack=ack))
