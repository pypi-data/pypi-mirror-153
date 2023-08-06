from typing import Optional

from cache.holder.RedisCacheHolder import RedisCacheHolder
from core.exchange.InstrumentExchange import InstrumentExchange
from core.number.BigFloat import BigFloat
from core.options.exception.MissingOptionError import MissingOptionError
from coreutility.collection.dictionary_utility import as_data

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

    def __build_key(self):
        return self.options[INSTRUMENT_TRADE_FEE_KEY]

    def retrieve_instrument_trade_fee(self, instrument_exchange) -> Optional[BigFloat]:
        instrument_trade_fees = self.retrieve_all()
        trade_fee = as_data(instrument_trade_fees, str(instrument_exchange))
        return BigFloat(trade_fee) if trade_fee is not None else None

    def store_instrument_trade_fee(self, fee, instrument_exchange):
        key = self.__build_key()
        instrument_trade_fees = self.retrieve_all()
        instrument_trade_fees[str(instrument_exchange)] = str(fee)
        self.cache.store(key, instrument_trade_fees)

    def retrieve_all(self):
        key = self.__build_key()
        instrument_trade_fees = self.cache.fetch(key, as_type=dict)
        if instrument_trade_fees is None:
            instrument_trade_fees = {}
        return instrument_trade_fees

