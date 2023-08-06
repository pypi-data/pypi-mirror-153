from cache.holder.RedisCacheHolder import RedisCacheHolder
from core.number.BigFloat import BigFloat
from core.options.exception.MissingOptionError import MissingOptionError

INSTRUMENT_TRADE_FEE_KEY = 'INSTRUMENT_TRADE_FEE_KEY'


class InstrumentFeeRepository:

    def __init__(self, options):
        self.options = options
        self.__check_options()
        self.cache = RedisCacheHolder()

    def __check_options(self):
        if self.options is None:
            raise MissingOptionError(f'missing option please provide options {INSTRUMENT_TRADE_FEE_KEY}')
        if INSTRUMENT_TRADE_FEE_KEY not in self.options:
            raise MissingOptionError(f'missing option please provide option {INSTRUMENT_TRADE_FEE_KEY}')

    def __build_key(self, instrument):
        return self.options[INSTRUMENT_TRADE_FEE_KEY].format(instrument=instrument)

    def retrieve_instrument_trade_fee(self, instrument) -> BigFloat:
        key = self.__build_key(instrument)
        return self.cache.fetch(key, as_type=BigFloat)

    def store_instrument_trade_fee(self, fee, instrument):
        key = self.__build_key(instrument)
        self.cache.store(key, fee)
