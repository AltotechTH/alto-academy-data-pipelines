if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@custom
def create(*args, **kwargs):
    """
    """
    timescaledb_db_name = kwargs.get("timescaledb_db_name", None)
    if timescaledb_db_name is None:
        raise Exception(f"Please provide timescaleDB database name.")
    timescaledb_username = kwargs.get("timescaledb_username", None)
    if timescaledb_username is None:
        raise Exception(f"Please provide timescaleDB database username.")
    timescaledb_password = kwargs.get("timescaledb_password", None)
    if timescaledb_password is None:
        raise Exception(f"Please provide timescaleDB database password.")
    timescaledb_host = kwargs.get("timescaledb_host", None)
    if timescaledb_host is None:
        raise Exception(f"Please provide timescaleDB database host.")
    timescaledb_port = kwargs.get("timescaledb_port", 5432)
    if timescaledb_port is None:
        raise Exception(f"Please provide timescaleDB database port.")
    timescaledb_destination_table = kwargs.get("timescaledb_destination_table", None)
    if timescaledb_port is None:
        raise Exception(f"Please provide timescaleDB database table.")

    from alto_academy_workshop.utils.database import AltoTimescaleDB
    timescaleDB = AltoTimescaleDB(
        db_name=timescaledb_db_name,
        username=timescaledb_username,
        password=timescaledb_password,
        host=timescaledb_host,
        port=timescaledb_port
    )

    # list of dict for columns definition
    columns_config = [
        {"name": "timestamp", "type": "TIMESTAMPTZ NOT NULL"},
        {"name": "device_id", "type": "VARCHAR(128) NOT NULL"},
        {"name": "aggregation_type", "type": "VARCHAR(32)"},
        {"name": "datapoint", "type": "VARCHAR(64) NOT NULL"},
        {"name": "value", "type": "TEXT"},
    ]

    timescaleDB.create_table(
        table_name=timescaledb_destination_table,
        columns_config=columns_config,
        time_column="timestamp",
        chunk_interval="1 day",
    )

    return True
