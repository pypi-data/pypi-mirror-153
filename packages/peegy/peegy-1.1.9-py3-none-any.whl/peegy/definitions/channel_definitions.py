class ChannelType:
    EEG = 'EEG'
    MEG = 'MEG'
    EOG = 'EOG'
    artificial = 'artificial'
    Event = 'Event'
    none = None


class Domain(object):
    time = 'time'
    frequency = 'frequency'
    time_frequency = 'time_frequency'


class ElectrodeType(object):
    scalp = 'scalp'
    oeg = 'oeg'
    artificial = 'artificial'


class ChannelItem(object):
    def __init__(self,
                 idx=None,
                 x=None,
                 y=None,
                 z=None,
                 w=None,
                 h=None,
                 label='',
                 type=ChannelType.EEG,
                 valid=True,
                 fixed_polarity=False):
        self.idx = idx
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.h = h
        self.label = label
        self.type = type
        self.valid = valid
        # if fixed_polarity is true the polarity of this channel will not be reversed when required
        self.fixed_polarity = fixed_polarity
