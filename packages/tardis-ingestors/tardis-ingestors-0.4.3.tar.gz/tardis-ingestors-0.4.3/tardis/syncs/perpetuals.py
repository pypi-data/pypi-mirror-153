def sync_perpetuals(
    exchange: str,
    period_seconds: int,
    db_credentials: dict,
    tardis_api_key: str,
    max_days: int = 2,
    first_date: str = None,
):
    from tardis.ingestors.perpetuals_ingestor import PerpetualsTardisIngestor

    # Initialize
    ingestor = PerpetualsTardisIngestor(
        exchange, period_seconds, db_credentials, tardis_api_key
    )
    ingestor.sync(max_days, first_date)
