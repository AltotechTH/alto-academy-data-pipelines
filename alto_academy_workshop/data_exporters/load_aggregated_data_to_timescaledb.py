if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data(data_and_table, *args, **kwargs):
    """
    Insert the given data into TimescaleDB table.
    """
    data, _ = data_and_table  # Unpack the inputs
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
    
    if not data:
        print('The list of data is empty')
        raise Exception('The list of data is empty')


    try:
        timescaleDB.insert_data(table_name=timescaledb_destination_table, data=data)
        print(f"Successfully inserted {len(data)} row(s) of data into TimescaleDB")
    except Exception as e:
        print(f"Cannot insert data to TimescaleDB due to the follow error {e}")
        raise Exception(f"Cannot insert data to TimescaleDB due to the follow error {e}")

