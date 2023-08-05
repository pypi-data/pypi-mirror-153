import pandas as pd


class TestType(object):
    hotelling_t2_time = 'hotelling_t2_time'  # hotelling-t2 test in the time-domain
    hotelling_t2_freq = 'hotelling_t2_freq'  # hotelling-t2 test in the frequency-domain
    f_test_freq = 'f_test_freq'  # f-ratio in frequency domain
    f_test_time = 'f_test_time'  # f-ratio using multiple points in the time-domain
    rayleigh_test = 'rayleigh_test'  # phase-locking value
    covariance = 'covariance'  # covariance

    def get_available_methods(self):
        members = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]
        return members


class StatisticalTests(dict):
    def __init__(self, tests: dict = {}):
        super(StatisticalTests, self).__init__(self)
        for _key, _value in tests.items():
            self.append(_value, _key)

    def __setitem__(self, key, value):
        assert isinstance(value, pd.DataFrame)
        key = self.ensure_unique_name(label=key)
        super(StatisticalTests, self).__setitem__(key, value)
        # we add the new item as class variable
        setattr(self, key, value)
        # set name of InoutOutputProcess
        value.name = key

    def append(self, test: pd.DataFrame, name=None):
        assert name is not None
        self[name] = test

    def ensure_unique_name(self, label: str = None):
        all_names = [_key for _key in self.keys()]
        _label = label
        count = 0
        while _label in all_names:
            _label = label + '_' + str(count)
            count = count + 1
        if count > 0:
            print('Statistical test "{:}" already exists. Renamed to "{:}"'.format(label, _label))
        return _label


class HotellingTSquareFrequencyTest(object):
    def __init__(self,
                 test_name='HT2',
                 frequency_tested=None,
                 df_1=None,
                 df_2=None,
                 t_square=None,
                 f=None,
                 p_value=None,
                 n_epochs=None,
                 spectral_magnitude=None,
                 spectral_phase=None,
                 rn=None,
                 snr=None,
                 snr_db=None,
                 f_critic=None,
                 channel=None):
        self.test_name = test_name
        self.frequency_tested = frequency_tested
        self.df_1 = df_1
        self.df_2 = df_2
        self.t_square = t_square
        self.f = f
        self.p_value = p_value
        self.spectral_magnitude = spectral_magnitude
        self.spectral_phase = spectral_phase
        self.rn = rn
        self.n_epochs = n_epochs
        self.snr = snr
        self.snr_db = snr_db
        self.f_critic = f_critic
        self.channel = channel


class HotellingTSquareTest(object):
    def __init__(self,
                 test_name='HT2',
                 df_1=None,
                 df_2=None,
                 t_square=None,
                 f=None,
                 f_critic=None,
                 p_value=None,
                 mean_amplitude=None,
                 mean_phase=None,
                 rn=None,
                 n_epochs=None,
                 snr=None,
                 snr_db=None,
                 snr_critic_db=None,
                 snr_critic=None,
                 channel=None,
                 frequency_tested=None,
                 **kwargs
                 ):
        self.test_name = test_name
        self.df_1 = df_1
        self.df_2 = df_2
        self.t_square = t_square
        self.f = f
        self.f_critic = f_critic
        self.p_value = p_value
        self.mean_amplitude = mean_amplitude
        self.mean_phase = mean_phase
        self.rn = rn
        self.n_epochs = n_epochs
        self.snr = snr
        self.snr_db = snr_db
        self.snr_critic_db = snr_critic_db
        self.snr_critic = snr_critic
        self.channel = channel
        self.frequency_tested = frequency_tested
        for _item, _value in kwargs.items():
            setattr(self, _item, _value)


class FrequencyFTest(object):
    def __init__(self,
                 test_name='F-test',
                 frequency_tested=None,
                 df_1=None,
                 df_2=None,
                 f=None,
                 p_value=None,
                 spectral_magnitude=None,
                 spectral_phase=None,
                 rn=None,
                 snr=None,
                 snr_db=None,
                 f_critic=None,
                 channel=None):
        self.test_name = test_name
        self.frequency_tested = frequency_tested
        self.df_1 = df_1
        self.df_2 = df_2
        self.f = f
        self.p_value = p_value
        self.spectral_magnitude = spectral_magnitude
        self.spectral_phase = spectral_phase
        self.rn = rn
        self.snr = snr
        self.snr_db = snr_db
        self.f_critic = f_critic
        self.channel = channel


class PhaseLockingValueTest(object):
    def __init__(self,
                 test_name='rayleigh_test',
                 plv=None,
                 df_1=None,
                 z_value=None,
                 z_critic=None,
                 p_value=None,
                 mean_phase=None,
                 channel=None,
                 frequency_tested=None,
                 rn=None):
        self.test_name = test_name
        self.plv = plv
        self.df_1 = df_1
        self.z_value = z_value
        self.z_critic = z_critic
        self.p_value = p_value
        self.mean_phase = mean_phase
        self.channel = channel
        self.frequency_tested = frequency_tested
        self.rn = rn


class FpmTest(object):
    def __init__(self,
                 test_name='Fmp',
                 label: str = None,
                 df_1: float = None,
                 df_2: float = None,
                 f: float = None,
                 f_critic: float = None,
                 p_value: float = None,
                 rn: float = None,
                 snr: float = None,
                 time_ini: float = None,
                 time_end: float = None,
                 n_epochs: int = None,
                 channel: str = None):
        self.test_name = test_name
        self.label = label
        self.df_1 = df_1
        self.df_2 = df_2
        self.f = f
        self.f_critic = f_critic
        self.p_value = p_value
        self.rn = rn
        self.snr = snr
        self.time_ini = time_ini
        self.time_end = time_end
        self.n_epochs = n_epochs
        self.channel = channel
