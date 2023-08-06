import binascii
from acomms.cyclestats import CycleStats
from acomms.index_list import IndexList

class FDPacket(object):
    def __init__(self, src, dest, miniframe_rate, dataframe_rate, ack,
                 cyclestats=None, miniframes=None, dataframes=None,
                 minibytes=None, databytes=None, version=7):

        if miniframes is not None and minibytes is not None:
            raise ValueError("FDPacket should only be initialized from received frames or simply the desired bytes")

        if dataframes is not None and databytes is not None:
            raise ValueError("FDPacket should only be initialized from received frames or simply the desired bytes")

        self.src = src
        self.dest = dest
        self.miniframe_rate = miniframe_rate
        self.dataframe_rate = dataframe_rate
        self.ack = ack
        self.version = version

        self.cyclestats = cyclestats

        if miniframes is None and minibytes is None:
            self.miniframes = []

        if dataframes is None and databytes is None:
            self.dataframes = []

        if minibytes is not None:
            self._minibytes = bytes(minibytes)
        else:
            self._minibytes = bytes()

        if databytes is not None:
            self._databytes = bytes(databytes)
        else:
            self._databytes = bytes()

    @property
    def packet_is_good(self):
        if self._minibytes or self._databytes:
            return True
        else:
            packet_is_good = True
            if self.miniframes:
                packet_is_good = packet_is_good and bool(min([miniframe.crccheck for miniframe in self.miniframes]))
            if self.dataframes:
                packet_is_good = packet_is_good and bool(min([dataframe.crccheck for dataframe in self.dataframes]))

            return packet_is_good

    @property
    def minibytes(self):
        if self._minibytes:
            return self._minibytes
        return bytes().join([miniframe.data for miniframe in self.miniframes])

    @property
    def databytes(self):
        if self._databytes:
            return self._databytes
        return bytes().join([frame.data for frame in self.dataframes])

    @property
    def valid_minibytes(self) -> IndexList:
        return self.get_valid_index(self.miniframes)

    @property
    def valid_databytes(self) -> IndexList:
        return self.get_valid_index(self.dataframes)

    def get_valid_index(self, frames) -> IndexList:
        valid_index = IndexList()

        idx = 0

        if len(frames) > 0:
            for frame in frames:
                length = frame.nbytes
                start = idx
                end = idx + length

                if frame.crccheck:
                    valid_index.append([start, end])

                idx = idx + length

            #valid_index.simplify()

        return valid_index

    def parse_frames(self, framestring):
        framelist = []

        framesplit = framestring.split(';')
        nframes = int(len(framesplit)/3)

        for i in range(0, nframes):
            framelist.append(FDFrame(int(framesplit[i*3]) == 1,
                                     int(framesplit[i*3+1]),
                                     bytearray.fromhex(framesplit[i*3+2])))

        return framelist

    def load_legacy_frames(self, legacyframes):
        framelist = []

        nframes = int(len(legacyframes))

        for i in range(0, nframes):
            framelist.append(FDFrame(~legacyframes[i].bad_crc, len(legacyframes[i].data), legacyframes[i].data))

        self.dataframes = framelist

    def add_miniframes(self, miniframestring):
        self.miniframes = self.miniframes + self.parse_frames(miniframestring)

    def add_dataframes(self, dataframestring):
        self.dataframes = self.dataframes + self.parse_frames(dataframestring)

    def add_cyclestats(self, cyclestats):
        self.cyclestats = cyclestats

    def msg_tfp(self, ver_pass):
        if ver_pass:
            msg = {'type': 'CCTFP', 'params': [0,
                                               0,
                                               self.dest,
                                               self.miniframe_rate,
                                               self.dataframe_rate,
                                               self.ack,
                                               0,
                                               self._minibytes.hex(),
                                               self._databytes.hex()]}

        else:
            msg = {'type': 'CCTFP', 'params': [self.dest,
                                               self.miniframe_rate,
                                               self.dataframe_rate,
                                               self.ack,
                                               0,
                                               self._minibytes.hex(),
                                               self._databytes.hex()]}

        return msg

    def msg_tdp(self):
        msg = {'type': 'CCTDP', 'params': [self.dest,
                                           self.dataframe_rate,
                                           0,
                                           0,
                                           self._databytes.hex()]}
        return msg

class FDFrame(object):
    def __init__(self, crccheck, nbytes, data):
        self.crccheck = crccheck
        self.nbytes = nbytes
        self.data = bytearray(data)
