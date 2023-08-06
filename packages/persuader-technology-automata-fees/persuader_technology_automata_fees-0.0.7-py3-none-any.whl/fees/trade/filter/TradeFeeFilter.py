from core.number.BigFloat import BigFloat


class TradeFeeFilter:

    def obtain_account_trade_fee(self) -> BigFloat:
        pass

    def obtain_instrument_trade_fee(self, instrument) -> BigFloat:
        pass
