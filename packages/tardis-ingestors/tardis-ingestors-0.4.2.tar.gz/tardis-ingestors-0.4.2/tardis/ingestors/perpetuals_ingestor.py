from datetime import datetime, timedelta
from typing import List, Optional, Tuple

import pandas as pd
from tardis.database.table import ConstanceDBTable
from tardis.ingestors.base_ingestor import BaseTardisIngestor
from tardis.models.outputs.data_types import DerivativeTicker
from tardis.utils import get_utc_timestamp


class PerpetualsTardisIngestor(BaseTardisIngestor):
    SYMBOL = "PERPETUALS"
    TABLE_TYPE = "perpetuals"

    def _get_table(self, exchange: str, period: timedelta) -> ConstanceDBTable:
        exchange = exchange.split("-")[0]
        return self.db_client.get_table(self.TABLE_TYPE, period, exchange)

    def _get_symbol(self) -> str:
        return self.SYMBOL

    def _get_time_cols(self) -> List[str]:
        return ["timestamp", "funding_timestamp"]

    def _get_latest_snapshot(self) -> List[DerivativeTicker]:
        latest_timestamp = self.table.get_latest_time()
        if latest_timestamp is None:
            return []
        snapshot = self.table.get_snapshot(latest_timestamp)
        return [
            DerivativeTicker(
                timestamp=get_utc_timestamp(latest_timestamp),
                exchange=self.tardis_client.exchange.value,
                symbol=row["symbol"],
                funding_timestamp=(
                    int(row["funding_timestamp"].timestamp() * 1e6)
                    if row["funding_timestamp"]
                    else None
                ),
                funding_rate=row["funding_rate"],
                predicted_funding_rate=row["predicted_funding_rate"],
                open_interest=row["open_interest"],
                last_price=row["last_price"],
                index_price=row["index_price"],
                mark_price=row["mark_price"],
            )
            for _, row in snapshot.iterrows()
        ]

    def _get_sync_range(
        self, max_days: int, first_date: Optional[datetime] = None
    ) -> Tuple[datetime, datetime]:
        range_start, range_end = self._get_symbol_datetime_range()
        if first_date is not None:
            range_start = max(range_start, first_date)
        latest_time = self.table.get_latest_time()
        sync_start = latest_time if latest_time else range_start
        sync_end = min(sync_start + timedelta(days=max_days), range_end)
        return sync_start, sync_end

    def _get_data(
        self, max_days: int, first_date: Optional[datetime] = None
    ) -> Optional[pd.DataFrame]:
        print(f"Syncying {self.SYMBOL} for max days {max_days}")
        sync_start, sync_end = self._get_sync_range(max_days, first_date)
        print(f"Syncing {sync_start} to {sync_end}")
        if sync_start + self.period >= sync_end:  # Skip if no new data
            print(f"No new data for {self.SYMBOL}")
            return

        return self.tardis_client.generate_perpetuals_derivative_ticker_snapshots(
            from_datetime=sync_start,
            to_datetime=sync_end,
            snapshot_interval=self.period,
            previous_snapshot=self._get_latest_snapshot(),
        )
