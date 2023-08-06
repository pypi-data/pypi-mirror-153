from cache.holder.RedisCacheHolder import RedisCacheHolder
from core.number.BigFloat import BigFloat
from core.options.exception.MissingOptionError import MissingOptionError

ACCOUNT_TRADE_FEE_KEY = 'ACCOUNT_TRADE_FEE_KEY'


class AccountFeeRepository:

    def __init__(self, options):
        self.options = options
        self.__check_options()
        self.cache = RedisCacheHolder()

    def __check_options(self):
        if self.options is None:
            raise MissingOptionError(f'missing option please provide options {ACCOUNT_TRADE_FEE_KEY}')
        if ACCOUNT_TRADE_FEE_KEY not in self.options:
            raise MissingOptionError(f'missing option please provide option {ACCOUNT_TRADE_FEE_KEY}')

    def retrieve_account_trade_fee(self) -> BigFloat:
        key = self.options[ACCOUNT_TRADE_FEE_KEY]
        return self.cache.fetch(key, as_type=BigFloat)

    def store_account_trade_fee(self, fee):
        key = self.options[ACCOUNT_TRADE_FEE_KEY]
        self.cache.store(key, fee)
