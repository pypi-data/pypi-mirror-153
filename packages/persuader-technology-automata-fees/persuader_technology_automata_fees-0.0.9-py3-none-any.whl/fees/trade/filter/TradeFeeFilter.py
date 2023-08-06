from typing import Optional

from core.number.BigFloat import BigFloat


class TradeFeeFilter:

    def obtain_account_trade_fee(self) -> Optional[BigFloat]:
        pass

    def obtain_instrument_trade_fee(self, instrument_exchange) -> Optional[BigFloat]:
        pass
