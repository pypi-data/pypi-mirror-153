from core.number.BigFloat import BigFloat

from feerepo.repository.account.AccountFeeRepository import AccountFeeRepository
from feerepo.repository.exception.NoTradeFeeError import NoTradeFeeError
from feerepo.repository.instrument.InstrumentFeeRepository import InstrumentFeeRepository


class FeeRepository:

    def __init__(self, options):
        self.account_repository = AccountFeeRepository(options)
        self.instrument_repository = InstrumentFeeRepository(options)

    def get_trade_fee(self, instrument_exchange) -> BigFloat:
        fee = self.instrument_repository.retrieve_instrument_trade_fee(instrument_exchange)
        if fee is None:
            fee = self.account_repository.retrieve_account_trade_fee()
        if fee is None:
            raise NoTradeFeeError(f'Trade Fee cannot be found at instrument or account level for [{instrument_exchange}]')
        return fee
