from acomms.flexibledataprotocol import FDPacket, FDFrame
from acomms.pid_defs import *
from acomms.index_list import IndexList

class NetPacket(object):

    def __init__(self, link_src = None, link_dest = None,
                 header_valid=False, header_bytes=None,
                 valid_index: IndexList = None, data_bytes=None):

        self.link_src = link_src
        self.link_dest = link_dest

        self.header_valid = header_valid

        if data_bytes is None and valid_index is not None:
            raise ValueError("valid_index requires data_bytes")

        if header_bytes is not None:
            self.header_bytes = header_bytes
        else:
            self.header_bytes = []

        if valid_index is not None:
            self.valid_index = valid_index
        elif valid_index is None and data_bytes is not None:
            self.valid_index = IndexList([0, len(data_bytes)])

        if data_bytes is not None:
            self.data_bytes = data_bytes
        else:
            self.data_bytes = []

        self.subheaders = {}

        if self.header_valid:
            self.subheaders, idx = self._split_header(self.header_bytes)

    @classmethod
    def from_fdpacket(cls, fdpacket: FDPacket):
        netpacket = cls()

        netpacket._init_header(fdpacket)
        netpacket._init_data(fdpacket)

        if netpacket.header_valid:
            netpacket.subheaders, idx = netpacket._split_header(netpacket.header_bytes)

        netpacket.link_src = fdpacket.src
        netpacket.link_dest = fdpacket.dest

        return netpacket

    def to_fdpacket(self, miniframerate=1, dataframerate=1, ack=False):
        fdpacket = FDPacket(self.link_src, self.link_dest,
                            miniframerate, dataframerate, ack,
                            minibytes=self.header_bytes, databytes=self.data_bytes)

        return fdpacket

    def _init_header(self, fdpacket: FDPacket):
        #if not fdpacket.miniframes:
            #self._init_header_data_legacy(fdpacket)
        #else:

        valid_index, header = self._combine_frames(fdpacket.miniframes)

        # If there are missing bytes in the header, we can't really use it
        if len(valid_index) != 1:
            self.header_valid = False
        # Also be sure the index covers full length of header
        elif valid_index[0][-1] != len(header):
            self.header_valid = False
        else:
            self.header_bytes = header
            self.header_valid = True

    def _init_data(self, fdpacket: FDPacket):
        # If we can't parse the header, nothing to do with this data
        if not self.header_valid:
            return

        # If fdpacket.miniframes is non populated we already parsed
        # header and data together in legacy configuration
        if not fdpacket.miniframes:
            return

        valid_index, data = self._combine_frames(fdpacket.dataframes)

        self.data_bytes = data
        self.valid_index = valid_index

    def _init_header_data_legacy(self, fdpacket):
        # If the first dataframe failed, we can't parse the header.
        if not fdpacket.dataframes[0].crccheck:
            self.header_valid = False
        else:
            valid_index, mixed_bytes = self._combine_frames(fdpacket.dataframes)

            subheaders, idx = self._split_header(mixed_bytes)

            if subheaders is not None:
                idx = idx+1
                self.header_bytes = mixed_bytes[0:idx]
                self.data_bytes = mixed_bytes[idx:]

                # Modify valid index for new data_byte index
                for i in range(len(valid_index)):
                    for k in range(len(valid_index[i])):
                        valid_index[i][k] = valid_index[i][k] - idx
                        if valid_index[i][k] < 0:
                            valid_index[i][k] = 0

                # Remove elements in index that are out of bounds
                new_index = []
                for i in range(len(valid_index)):
                    if valid_index[i][-1] > 0:
                        new_index.append(valid_index[i])

    def _split_header(self, headerbytes, valid_index = None):
        subheaders = dict()
        idx = 0
        while idx < len(headerbytes):
            # Check if we've exceeded the valid index for these bytes
            if valid_index is not None:
                if idx > valid_index[0][-1]:
                    return None, None
            # If we reached terminator PID, no more subheaders
            if headerbytes[idx] == END_PID:
                break
            # If the PID is in vetted address space, we should know the length
            if headerbytes[idx] < FIRST_PROTO_PID:
                pass  # TODO: PID length lookup from pid_defs.py
            # Else we are in prototype PID space, so use included length field
            else:
                subheaders[headerbytes[idx]] = headerbytes[idx: idx + headerbytes[idx + 1]]
                idx = idx + headerbytes[idx + 1]

        return subheaders, idx

    def _combine_frames(self, frames):
        valid_index = IndexList()
        fbytes = bytearray()

        idx = 0

        if len(frames) > 0:
            for frame in frames:
                length = frame.nbytes
                start = idx
                end = idx + length

                if frame.crccheck:
                    valid_index.append([start, end])
                    fbytes = fbytes + frame.data
                else:
                    fbytes = fbytes + bytearray(length)

                idx = idx + length

            #TODO: handle case where all frame CRC checks fail
            valid_index.simplify()

        return valid_index, fbytes
