class Ping(dict):

    fields = ('type',
              'src', 'dest',
              'rate',
              'isodate',
              'snr_in', 'snr_out',
              'owtt',
              'tx_level',
              'reserved1', 'reserved2',
              'timestamp_res', 'toa_mode',
              'snv_on', 'timestamp'
               )


    def __getattr__(self, item):
        """Maps values to attributes.
        Only called if there *isn't* an attribute with this name
        """
        try:
            return self.__getitem__(item)
        except KeyError:
            raise AttributeError(item)

    def __setattr__(self, item, value):
        """Maps attributes to values.
        Only if we are initialised
        """
        if self.__dict__.__has_key(item):
            dict.__setattr__(self, item, value)
        else:
            self.__setitem__(item, value)

    def __str__(self):
        hrstr = "{ts}\tSRC: {src: .0f}\tDST: {dst: .0f}\tOWTT: {owtt: .0f}\tSNR_out: {snr_out: .0f}\tTX_Level: {txlvel: .0f}".format(
            ts = self['isodate'], src = self['src'], dst = self['dest'], owtt = self['owtt'], snr_out = self['snr_out'], txlvel = self['tx_level'])

        return hrstr

    @classmethod
    def from_nmea_msg(cls, msg, modem):
        print(msg['type'])

        if not modem.fw_at_least("v3.0.0"):
            if msg['type'] == "CACMD":
                return cls(Ping.from_cacmd_msg(cls, msg, modem))
            elif msg['type'] == "CACMA":
                return cls(Ping.from_cacma_msg(cls, msg, modem))
        elif msg['type'] == "CACMA":
                return cls(Ping.from_cacma_msg(cls, msg, modem))
        elif msg['type'] == "CACMR":
                return cls(Ping.from_cacmr_msg(cls, msg, modem))

        modem._daemon_log.error("Ping: unrecognized nmea message.")
        return None

    def from_cacmd_msg(cls, msg, modem):
        values = dict.fromkeys(Ping.fields)

        if not modem.fw_at_least("v3.0.0"):
            if msg["params"][0] == "PNG":
                values['type'] = msg['params'][0]
                values['src'] = int(msg["params"][1])
                values['dest'] = int(msg["params"][2])
                values['rate'] = int(msg["params"][3])
                values['cdr'] = int(msg["params"][4])
            elif msg["params"][1] == "PNR":
                values['type'] = msg['params'][1]
                values['src'] = int(msg["params"][2])
                values['dest'] = int(msg["params"][3])
                values['owtt'] = float(msg["params"][4])
                values['snr_in'] = float(msg["params"][5])
                values['snr_out'] = float(msg["params"][6])
                values['tx_level'] = int(msg["params"][7])
                values['reserved1'] = int(msg["params"][8])
                values['reserved2'] = int(msg["params"][8])

            return values
        else:
            modem._daemon_log.error("Modem acknowledges ping command requested. Shouldn't try to parse")
            return None

    def from_cacma_msg(cls, msg, modem):
        values = dict.fromkeys(Ping.fields)
        if not modem.fw_at_least("v3.0.0"):
            values['isodate'] = msg['params'][0]
            values['type'] = msg['params'][1]

        else:
            values['type'] = msg['params'][0]
            values['isodate'] = msg['params'][1]

        values['src'] = int(msg['params'][2])
        values['dest'] = int(msg['params'][3])
        values['snr_in'] = float(msg['params'][4])
        values['snr_out'] = float(msg['params'][5])
        values['tx_lvel'] = float(msg['params'][6])
        values['reserved1'] = msg['params'][7]
        values['reserved2'] = msg['params'][8]

        return values

    def from_cacmr_msg(cls, msg, modem):
        values = dict.fromkeys(Ping.fields)

        values['type'] = msg['params'][0]
        values['isodate'] = msg['params'][1]
        values['src'] = int(msg["params"][2])
        values['dest'] = int(msg["params"][3])
        values['owtt'] = float(msg["params"][4])
        values['snr_in'] = float(msg["params"][5])
        values['snr_out'] = float(msg["params"][6])
        values['tx_level'] = int(msg["params"][7])
        values['reserved1'] = int(msg["params"][8])
        time_fields = (msg["params"][9]).split(';')
        if len(time_fields) == 4:
            values['timestamp_res'] = int(time_fields[0])
            values['toa_mode'] = int(time_fields[1])
            values['snv_on'] = int(time_fields[2])
            values['timestamp'] = int(time_fields[3])

        return values

    def is_reply(self):
        if self['type'] == 'PNR':
            return True
        else:
            return False
