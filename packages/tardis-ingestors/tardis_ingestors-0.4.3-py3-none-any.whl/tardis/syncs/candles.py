def sync_candles(
    exchange: str,
    period_seconds: int,
    db_credentials: dict,
    tardis_api_key: str,
    max_days: int = 10,
):
    from tardis.ingestors.candle_ingestor import CandleTardisIngestor

    # Initialize
    ingestor = CandleTardisIngestor(
        exchange, period_seconds, db_credentials, tardis_api_key
    )
    ingestor.sync(max_days)
