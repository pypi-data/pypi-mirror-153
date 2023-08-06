from acomms.messageparams import CycleInfo, DrqParams, DataFrame, Ack, Causb2, Casst, data_from_hexstring, hexstring_from_data
from acomms.cyclestats import CycleStats, TransmitStats
from acomms.ping import Ping
from acomms.timeutil import *
from acomms.flexibledataprotocol import FDPacket, FDFrame
import sys
import traceback
import os

class MessageParser:
    def __init__(self, modem):
        self.modem = modem    
    
    # This method gets called when the object is called as a function, and
    # tries to find a matching attribute for that message type.
    # This is a pythonic(?) way of implementing a switch case.
    def parse(self, msg):
        try:
            func = getattr(self, msg['type'])
        except AttributeError as e:
            self.modem._daemon_log.warn('Unrecognized message: ' + str(msg['type']))
            func = None
        try:
            if func != None:
                return func(msg)
        except Exception as e:
            self.modem._daemon_log.error("Exception when parsing: " + str(sys.exc_info()[0]))
            traceback.print_exc()

    def GPRMC(self,msg):
        pass

    def CASFE(self,msg):
        pass

    def CASEN(self,msg):
        pass

    def CASIF(self,msg):
        pass

    def CASFL(self,msg):
        pass

    def PUBX(self,msg):
        pass

    def SNPGT(self,msg):
        pass

    def CACFG(self, msg):
        # Only worry about the parameters that matter...
        key = msg["params"][0]
        value = msg["params"][1]

        if key == "info.firmware_version":
            self.modem.fw_version = value
        
        if key == "SRC": self.modem.id = int(value)
        if key == "ASD": self.modem.asd = bool(int(value))
        if key == "PCM": self.modem.pcm_on = bool(int(value))
        self.modem.config_data[key] = value
        
    def CACYC(self, msg):
        src = int(msg["params"][1])
        dest = int(msg["params"][2])
        rate = int(msg["params"][3])
        ack = int(msg["params"][4]) == 1
        num_frames = int(msg["params"][5])
        
        cycleinfo = CycleInfo(src, dest, rate, ack, num_frames)
        
        # Pass this to the comms state machine.
        self.modem.state.got_cacyc(cycleinfo)
        
    def CATXF(self, msg):
        self.modem.state.got_catxf()
        
    def CADRQ(self, msg):
        src = int(msg["params"][1])
        dest = int(msg["params"][2])
        ack = int(msg["params"][3]) == 1
        num_bytes = int(msg["params"][4])
        frame_num = int(msg["params"][5]) 
        
        drqparams = DrqParams(src, dest, ack, num_bytes, frame_num)
        
        self.modem.state.got_cadrq(drqparams)
        
    def CARXD(self, msg):
        src = int(msg["params"][0])
        dest = int(msg["params"][1])
        ack = int(msg["params"][2]) == 1
        frame_num = int(msg["params"][3])
        data = data_from_hexstring(msg["params"][4])
        
        dataframe = DataFrame(src, dest, ack, frame_num, data)
        
        self.modem.state.got_carx(dataframe)
        self.modem.on_rxframe(dataframe)
        
    def CAMSG(self, msg):
        # CAMSG sucks.  We need to parse it to figure out what's going on.
        # This doesn't account for all of the possible CAMSG messages.
        if msg["params"][0] == "BAD_CRC":
            self.modem.state.got_badcrc()
        elif msg["params"][0] == "PACKET_TIMEOUT":
            self.modem.state.got_packettimeout()
        else:
            try:
                msg_type = msg["params"][0]
                number = int(msg["params"][1])
                self.modem.state.got_camsg(msg_type,number)
            except ValueError:
                pass
        #TODO: Add PSK errors here
            
    def CAERR(self, msg):
        # Sigh.  This really shouldn't be used to signal data timeouts, but it is.
        # This doesn't account for most of the CAERR messages.
        if msg["params"][1] == "DATA_TIMEOUT":
            frame_num = msg["params"][2]
            self.modem.state.got_datatimeout(frame_num)
        else:
            hhmmss = msg["params"][0]
            module = msg["params"][1]
            err_num = int(msg["params"][2])
            message = msg["params"][3]
            self.modem.state.got_caerr(hhmmss,module,err_num,message)
    
    def CAREV(self, msg):
        '''Revision Message'''
        self.modem.state.got_carev(msg)
        self.modem.on_carev(msg)
        
    def CATXP(self, msg):
        '''Start of Packet Transmission Acoustically'''
        pass
    
    def CAMPA(self,msg):
        '''Ping Received Acoustically'''
        src = int(msg["params"][0])
        dest = int(msg["params"][1])
        self.modem.state.got_campa(src,dest)
        pass

    def CADQF(self,msg):
        '''Data Quality Factor Message'''
        dqf= int(msg["params"][0])
        p = int(msg["params"][1])        
        self.modem.state.got_cadqf(dqf,p)
        pass
    
    def CARSP(self, msg):
        '''Echo of CCRSP command'''
        pass
    
    def CAXST(self, msg):
        '''Transmit Statistics message'''
        try:
            xst = TransmitStats.from_nmea_msg(msg)

            # Raise the event
            self.modem.on_xst(xst, msg)
        except Exception as ex:
            self.modem._daemon_log.error("Error parsing XST: " + str(sys.exc_info()[0]))
        pass
    
    def CARXP(self, msg):
        '''Probe received (RX pending)'''
        pass
    
    def CAMPC(self, msg):
        '''Ping command echo'''
        pass

    def CAMPR(self, msg):
        '''Ping command reply'''
        src = int(msg["params"][0])
        dest = int(msg["params"][1])
        owtt = float(msg["params"][2])

        campr = Campr(src=src, dest=dest, owtt=owtt)

        self.modem.on_campr(campr)
        pass
    
    def CAMUC(self, msg):
        '''User minipacket command echo'''
        pass
        
    def CAMUR(self, msg):
        '''User minipacket reply'''
        pass

    def CAMUA(self, msg):
        '''User minipacket received accoustically'''
        src = int(msg["params"][0])
        dest = int(msg["params"][1])
        data = data_from_hexstring(msg["params"][2])

        camua = Camua(src=src, dest=dest, data=data)

        self.modem.on_camua(camua)
        
    def CATXD(self, msg):
        '''CCTXD echo'''
        pass
        
    def CAMSC(self, msg):
        '''Sleep command echo'''
        pass

    def CATMS(self, msg):
        '''Time set command echo '''
        pass

    def CATMG(self, msg):
        '''Time status '''
        pass

    def CARBR(self, msg):
        '''Log message retreival
        '''
        pass

    def CAHIB(self, msg):
        '''hibernate echo
        '''
        pass

    def CAHBR(self, msg):
        '''Hibernate status
        '''
        pass

    def CAALQ(self, msg):
        '''API level query response
        '''
        pass

    def CACLK(self, msg):
        # $CACLK,yyyy,MM,dd,HH,mm,ss
        args = msg["params"]
        datestr = str(args[1]) + str(args[2]) + str(args[3]) + str(args[4]) + str(args[0]) + '.' + str(args[5])
        if self.modem.set_host_clock_flag == True:
            self.modem._daemon_log.warn("Setting host clock to: " + datestr)
            #TODO: This probably shouldn't be part of this module.
            os.system('/bin/date -u ' + datestr)
            self.modem.set_host_clock_flag = False

    def CACLQ(self, msg):
        # $CACLK,yyyy,MM,dd,HH,mm,ss
        args = msg["params"]
        datestr = "{:0>2d}{:0>2d}{:0>2d}{:0>2d}{:0>4d}.{:0>2d}".format(int(args[1]), int(args[2]), int(args[3]), int(args[4]), int(args[0]), int(args[5]))
        if self.modem.set_host_clock_flag == True:
            self.modem._daemon_log.warn("Setting host clock to: " + datestr)
            #TODO: This probably shouldn't be part of this module.
            os.system('/bin/date -u ' + datestr)
            self.modem.set_host_clock_flag = False


    def CACST(self, msg):
        try:
            cst = CycleStats.from_nmea_msg(msg)

            # Raise the event
            self.modem.on_cst(cst, msg)
        except Exception as ex:
            self.modem._daemon_log.error("Error parsing CST: " + str(sys.exc_info()[0]))
            raise

    def CATRC(self, msg):
        pass

    def CAACK(self, msg):
        src = int(msg["params"][0])
        dest = int(msg["params"][1])
        frame_num = int(msg["params"][2])
        ack = int(msg["params"][3]) == 1

        ack = Ack(src, dest, ack, frame_num)
        self.modem.on_ack(ack,msg)

    def CACDR(self, msg):
        src = int(msg["params"][2])
        dest = int(msg["params"][3])
        ack = Ack(src, dest,1,0)
        self.modem.on_ack(ack, msg)


    def CATOA(self, msg):
        pass

    def CABBD(self,msg):
        pass

    def CABDD(self, msg):
        pass

    def CATDP(self,msg):
        #errflag = int(msg["params"][0])
        #uniqueID = int(msg["params"][1])
        #dest = int(msg["params"][2])
        #rate = int(msg["params"][3])
        #ack = int(msg["params"][4]) == 1
        #reserved = int(msg["params"][5])

        #mfdata = (msg(["params"][6])).split(';')
        #dfdata = (msg(["params"][7])).split(';')
        pass

    def CATFP(self, msg):
        pass

    def CARDP(self, msg):
        src = int(msg["params"][0])
        dest = int(msg["params"][1])
        rate = int(msg["params"][2])
        ack = int(msg["params"][3]) == 1
        reserved = int(msg["params"][4])
        dataframes = msg["params"][5]

        self.modem.current_fdpacket = FDPacket(src, dest, None, rate, ack)
        self.modem.current_fdpacket.add_dataframes(dataframes)

        self.modem._daemon_log.debug("Received FPD Packet Data")

    def CARFP(self,msg):
        msgtime = msg["params"][0]
        seqnum = int(msg["params"][1])
        src = int(msg["params"][2])
        dest = int(msg["params"][3])
        minirate = int(msg["params"][4])
        datarate = int(msg["params"][5])
        ack = int(msg["params"][6])
        reserved = int(msg["params"][7])
        modemminiframes = msg["params"][8]
        miniframes = msg["params"][9]
        dataframes = msg["params"][10]
        # pidinfo = msg["params"][11]

        self.modem.current_fdpacket = FDPacket(src, dest, minirate, datarate, ack)
        self.modem.current_fdpacket.add_miniframes(miniframes)
        self.modem.current_fdpacket.add_dataframes(dataframes)

        self.modem._daemon_log.debug("Received RFP Packet Data")
        self.modem._daemon_log.debug("Miniframes: " + miniframes)
        self.modem._daemon_log.debug("Dataframes: " + dataframes)

    def CAUSB2(self, msg):
        try:
            df = msg["params"][0]
            iso8601_time = msg["params"][1]
            azimuth_deg = float(msg["params"][2])
            elevation_deg = float(msg["params"][3])
            owtt_s = float(msg["params"][4])
            timing_mode = int(msg["params"][5])

            ire0_r = float(msg["params"][6])
            ire0_i = float(msg["params"][7])
            ire1_r = float(msg["params"][8])
            ire1_i = float(msg["params"][9])
            ire2_r = float(msg["params"][10])
            ire2_i = float(msg["params"][11])
            ire3_r = float(msg["params"][12])
            ire3_i = float(msg["params"][13])

            ire0 = complex(ire0_r, ire0_i)
            ire1 = complex(ire1_r, ire1_i)
            ire2 = complex(ire2_r, ire2_i)
            ire3 = complex(ire3_r, ire3_i)

            ndetects = int(msg["params"][14])

            causb2 = Causb2(df, iso8601_time, azimuth_deg, elevation_deg, owtt_s, timing_mode,
                            ire0, ire1, ire2, ire3,
                            ndetects)

            self.modem.on_causb2(causb2, msg)

        except Exception as ex:
            self.modem._daemon_log.error("Error parsing CAUSB2: {}".format(ex))
            raise

    def CACMA(self, msg):
        try:
            if self.modem.fw_at_least("3.0.0"):
                type =  msg["params"][0]

                if type == "PNG":
                    ping = Ping.from_nmea_msg(msg, self.modem)
                    self.modem.on_ping(ping, msg)
                else:
                    self.modem._daemon_log.warn("Unrecognized CACMA type")
            else:
                type = msg["params"][1]

                if type == "PNG":
                    ping = Ping.from_nmea_msg(msg, self.modem)
                    self.modem.on_ping(ping, msg)
                else:
                    self.modem._daemon_log.warn("Unrecognized CACMA type")

        except Exception as ex:
            self.modem._daemon_log.error("Error parsing CMA: " + str(sys.exc_info()[0]))
            raise

    def CACMR(self,msg):
        try:
            type = msg["params"][0]

            if type == "PNR":
                ping = Ping.from_nmea_msg(msg, self.modem)
                self.modem.on_ping(ping, msg)
            else:
                self.modem._daemon_log.warn("Unrecognized CACMR type")

        except Exception as ex:
            self.modem._daemon_log.error("Error parsing CMR: " + str(sys.exc_info()[0]))
            raise

    def CAALQ(self,msg):
        app_name = msg["params"][0]
        nmea_api_level = int(msg["params"][1])
        self.modem._daemon_log.info("Modem API Information: Application Name: {0} API Level: {1}".format(app_name,nmea_api_level))

		
    def CAFDR(self,msg):
        src = int(msg["params"][0])
        dest = int(msg["params"][1])
        rate = int(msg["params"][2])
        ack = int(msg["params"][3]) == 1
        nbytes  = int(msg["params"][4])


    def CATMG(self,msg):
        dt = convert_to_datetime(msg["params"][0])
        clksrc = msg["params"][1]
        pps_source = msg["params"][2]

        self.modem._daemon_log.info("Modem Date and Time Message:{0}\tClock Source:{1}\tPPS Source:{2}".format(dt,clksrc.replace('_',' '),pps_source.replace('_',' ')))

    def CATMQ(self,msg):
        dt = convert_to_datetime(msg["params"][0])
        clksrc = msg["params"][1]
        pps_source = msg["params"][2]

        self.modem._daemon_log.info("Modem Date and Time Query Response:{0}\tClock Source:{1}\tPPS Source:{2}".format(dt,clksrc.replace('_',' '),pps_source.replace('_',' ')))

    def CAPAS(self,msg):
        passthrough_msg = msg["params"][0]

        self.modem._daemon_log.info("Pass Through Message Received: {0}".format(passthrough_msg))

    def CAPST(self,msg):
        pass

    def CAHIB(self,msg):
        hibernate_cause = int(msg["params"][0])
        hibernate_time = convert_to_datetime(msg["params"][1])
        wake_cause = int(msg["params"][2])
        wake_time = convert_to_datetime(msg["params"][3])
        self.modem._daemon_log.info("Modem Hibernate Ack: Hibernate({0},{1}), Wake({2},{3})".format(hibernate_cause,hibernate_time,wake_cause,wake_time))
        pass

    def CAMEC(self,msg):
        pass

    def CAHBR(self,msg):
        wake_time = convert_to_datetime(msg["params"][0])
        self.modem._daemon_log.info("Modem Hibernate Start: Wake@{0}".format(wake_time))

    def CATMS(self,msg):
        dt = None
        timed_out = int(msg["params"][0])
        if msg["params"][1] is not None:
            dt = convert_to_datetime(msg["params"][1])
        self.modem._daemon_log.info("Modem Set Clock Response: Timed Out:{0} Time Set To:{1}".format(timed_out,dt))

    def CARBS(self,msg):
        pass
        #try:
        #    log = ModemLog.from_nmea_msg(msg)

            # Raise the event
        #    self.modem.on_modem_log(log, msg)
        #except Exception, ex:
        #    self.modem._daemon_log.error("Error parsing Retrieved Modem Log Message: " + str(sys.exc_info()[0]))

    def CARBR(self,msg):
        pass
        #try:
        #    log = ModemLog.from_nmea_msg(msg)

            # Raise the event
        #    self.modem.on_modem_log(log, msg)
        #except Exception, ex:
        #    self.modem._daemon_log.error("Error parsing Retrieved Modem Log Message: " + str(sys.exc_info()[0]))

    def CAACM(self, msg):
        dest = int(msg["params"][0])
        rate = int(msg["params"][1])
        ack = int(msg["params"][2])
        cmd_str = msg["params"][3]

        self.modem._daemon_log.info("Response to acoustic NMEA Message Received, CMD sent: {0}".format(cmd_str))

    def CAACR(self, msg):
        reference_ver = '3.0.0'
        ver_pass = self.modem.fw_at_least(reference_ver)
        if ver_pass:
            dest = int(msg["params"][0])
            rate = int(msg["params"][1])
            cmd_str = msg["params"][2]
        else:
            cmd_str = msg["params"][0]
            src = int(msg["params"][1])
            dest = int(msg["params"][2])

        self.modem._daemon_log.info("Ack of acoustic NMEA Message Received, CMD reply: {0}".format(cmd_str))

    def CAACA(self, msg):
        dest = int(msg["params"][0])
        rate = int(msg["params"][1])
        ack = int(msg["params"][2])
        cmd_str = msg["params"][3]

        self.modem._daemon_log.info("Receipt of acoustic NMEA Message Received, CMD sent: {0}".format(cmd_str))

    def CAACF(self, msg):
        src = int(msg["params"][0])
        error_code = int(msg["params"][1])
        nmea_name = msg["params"][2]
        nmea_value = msg["params"][3]

    def CASST(self, msg):
        try:
            sst_version = int(msg["params"][0])
            in_water_spl_dB = float(msg["params"][1])
            detector = int(msg["params"][2])
            num_samples = int(msg["params"][3])

            summary = {}
            summary['min'] = float(msg["params"][4])
            summary['lower_quartile'] = float(msg["params"][5])
            summary['median'] = float(msg["params"][6])
            summary['upper_quartile'] = float(msg["params"][7])
            summary['max'] = float(msg["params"][8])
            summary['len'] = int(msg["params"][9])

            casst = Casst(
                sst_version=sst_version,
                in_water_spl_dB=in_water_spl_dB, 
                detector=detector, 
                num_samples=num_samples, 
                summary=summary,
                )

            self.modem.on_casst(casst, msg)

        except Exception as ex:
            self.modem._daemon_log.error("Error parsing CASST: {}".format(ex))


    def CAMIZ(self,msg):
        pass

    def SNTTA(self,msg):
        pass

    def SNMFD(self,msg):
        pass

    def CASED(self,msg):
        pass

    def CASEL(self,msg):
        pass

    def CASWT(self,msg):
        pass

    def CASDO(self,msg):
        pass

    def SNUTX(self,msg):
        pass

    def UPMFWA(self,msg):
        slot = int(msg["params"][0])
        data_loc = int(msg["params"][1])
        total_data_size = int(msg["params"][2])
        sha1_hash = msg["params"][3]
        self.modem._daemon_log.info("Modem Starting FW Update Process: Slot {}, {} bytes, SHA1 HASH = ({}).".format(slot,total_data_size,sha1_hash))
        pass

    def UPDATA(self,msg):
        nbytes_received = int(msg["params"][0])
        self.modem._daemon_log.info("Modem Received {} Bytes of Firmware File Upload.".format(nbytes_received))
        pass

    def UPDONE(self,msg):
        update_msg = msg["params"][0]
        self.modem._daemon_log.info("Modem FW Update Done: {}".format(update_msg))
        pass

    def UPERR(self,msg):
        errno = int(msg["params"][0])
        err_msg = msg["params"][1]
        self.modem._daemon_log.error("Modem FW Update Errored ({}): {}".format(errno,err_msg))
        pass

    def CACMD(self, msg):
        try:
            if self.modem.fw_at_least('v3.0.0'):
                type = msg["params"][0]

                if type == "PNG":
                    self.modem._daemon_log.debug("Modem acknowledges ping command requested.")
                elif type == "RLS":
                    self.modem._daemon_log.debug("Modem acknowledges release command requested.")
                else:
                    self.modem._daemon_log.warn("Unrecognized CACMD type")
            else:
                if msg["params"][0] == "PNG":
                    ping = Ping.from_nmea_msg(msg, self.modem)
                    self.modem.on_ping(ping, msg)
                elif msg["params"][1] == "PNR":
                    ping = Ping.from_nmea_msg(msg, self.modem)
                    self.modem.on_ping(ping, msg)
                elif msg["params"][0] == "RLS":
                    self.modem._daemon_log.debug("Modem acknowledges release command requested.")
                else:
                    self.modem._daemon_log.warn("Unrecognized CACMD type")

        except Exception as ex:
            self.modem._daemon_log.error("Error parsing CACMD: " + str(sys.exc_info()[0]))
            raise


