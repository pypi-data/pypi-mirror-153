import logging

from exchangerepo.repository.InstrumentExchangeRepository import InstrumentExchangeRepository
from feerepo.repository.account.AccountFeeRepository import AccountFeeRepository
from feerepo.repository.instrument.InstrumentFeeRepository import InstrumentFeeRepository

from fees.trade.filter.TradeFeeFilter import TradeFeeFilter


class TradeFeeProvider:

    def __init__(self, options, trade_fee_filter: TradeFeeFilter):
        self.log = logging.getLogger(__name__)
        self.options = options
        self.trade_fee_filter = trade_fee_filter
        self.instrument_exchange_repository = InstrumentExchangeRepository(options)
        self.account_fee_repository = AccountFeeRepository(options)
        self.instrument_fee_repository = InstrumentFeeRepository(options)

    def obtain_trade_fees(self):
        self.obtain_account_fees()
        self.obtain_instrument_fees()

    def obtain_account_fees(self):
        fee = self.trade_fee_filter.obtain_account_trade_fee()
        if fee is not None:
            self.log.debug(f'Storing account fee:{fee}')
            self.account_fee_repository.store_account_trade_fee(fee)

    def obtain_instrument_fees(self):
        instrument_exchanges_holder = self.instrument_exchange_repository.retrieve()
        instrument_exchanges = instrument_exchanges_holder.get_all()
        if len(instrument_exchanges) > 0:
            for instrument_exchange in instrument_exchanges:
                self.obtain_both_sides_of_exchange_fees(instrument_exchange)

    def obtain_both_sides_of_exchange_fees(self, instrument_exchange):
        fee = self.trade_fee_filter.obtain_instrument_trade_fee(instrument_exchange)
        inverse_fee = self.trade_fee_filter.obtain_instrument_trade_fee(instrument_exchange.invert())
        self.store_relevant_fee(fee, inverse_fee, instrument_exchange)
        self.store_relevant_fee(inverse_fee, fee, instrument_exchange.invert())

    def store_relevant_fee(self, fee, other_fee, instrument_exchange):
        if fee is not None:
            self.log.debug(f'Storing fee:{fee} for [{instrument_exchange}]')
            self.instrument_fee_repository.store_instrument_trade_fee(fee, instrument_exchange)
        elif other_fee is not None:
            self.log.debug(f'Storing fee:{other_fee} for [{instrument_exchange}]')
            self.instrument_fee_repository.store_instrument_trade_fee(other_fee, instrument_exchange)
