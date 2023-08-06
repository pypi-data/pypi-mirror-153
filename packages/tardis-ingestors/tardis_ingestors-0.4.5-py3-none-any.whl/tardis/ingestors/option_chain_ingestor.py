from datetime import datetime, timedelta
from typing import List, Optional, Tuple

import pandas as pd
from tardis.database.table import ConstanceDBTable
from tardis.ingestors.base_ingestor import BaseTardisIngestor
from tardis.models.exchange.grouped_symbols import GroupedSymbol
from tardis.models.outputs.data_types import InstrumentStatus
from tardis.utils import get_utc_timestamp


class OptionsChainTardisIngestor(BaseTardisIngestor):
    SYMBOL = GroupedSymbol.OPTIONS.value
    TABLE_TYPE = "chain"

    def _get_table(self, exchange: str, period: timedelta) -> ConstanceDBTable:
        return self.db_client.get_table(self.TABLE_TYPE, period, exchange)

    def _get_symbol(self) -> str:
        return self.SYMBOL

    def _get_time_cols(self) -> List[str]:
        return ["timestamp", "expiration"]

    def _get_latest_snapshot(self) -> List[InstrumentStatus]:
        latest_timestamp = self.table.get_latest_time()
        if latest_timestamp is None:
            return []
        snapshot = self.table.get_snapshot(latest_timestamp)
        return [
            InstrumentStatus(
                timestamp=get_utc_timestamp(latest_timestamp),
                exchange=self.tardis_client.exchange.value,
                symbol=row["symbol"],
                underlying=row["underlying"],
                type=row["type"],
                strike=row["strike"],
                expiration=int(row["expiration"].timestamp() * 1e6),
                open_interest=row["open_interest"],
                last_price=row["last_price"],
                bid_price=row["bid_price"],
                bid_amount=row["bid_amount"],
                bid_iv=row["bid_iv"],
                ask_price=row["ask_price"],
                ask_amount=row["ask_amount"],
                ask_iv=row["ask_iv"],
                mark_price=row["mark_price"],
                mark_iv=row["mark_iv"],
                underlying_index=row["underlying_index"],
                underlying_price=row["underlying_price"],
                delta=row["delta"],
                gamma=row["gamma"],
                vega=row["vega"],
                theta=row["theta"],
                rho=row["rho"],
            )
            for _, row in snapshot.iterrows()
        ]

    def _get_data(
        self, max_days: int, first_date: Optional[datetime] = None
    ) -> Optional[pd.DataFrame]:
        sync_start, sync_end = self._get_sync_range(max_days, first_date, True)
        if sync_start + self.period >= sync_end:  # Skip if no new data
            print(f"No new data for {self.SYMBOL}")
            return

        return self.tardis_client.generate_option_chain_snapshots(
            from_datetime=sync_start,
            to_datetime=sync_end,
            snapshot_interval=self.period,
            previous_snapshot=self._get_latest_snapshot(),
        ).drop(columns=["exchange"])
