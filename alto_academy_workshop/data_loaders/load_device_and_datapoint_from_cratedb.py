if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

# import database utilities
from alto_academy_workshop.utils.database import AltoCrateDB

@data_loader
def load_data(*args, **kwargs):
    """
    loading device and datapoint from CrateDB.

    Returns:
        data frame
    """
    cratedb_host = kwargs.get("cratedb_host", "host.docker.internal")
    cratedb_port = kwargs.get("cratedb_port", 4200)
    if isinstance(cratedb_port, str):
        try:
            cratedb_port = int(cratedb_port)
        except Exception as e:
            print("port number could only be integer.")
            return None
    cratedb_source_table = kwargs.get("cratedb_source_table", None)
    if cratedb_source_table is None:
        print("CrateDB source table is not provided. Please provide the soure table.")
        return None
    query_period_seconds = kwargs.get("query_period_seconds", 60)
    if isinstance(query_period_seconds, str):
        query_period_seconds = int(query_period_seconds)

    cratedb = AltoCrateDB(
        host=cratedb_host,
        port=cratedb_port
    )

    start_timestamp = kwargs['interval_start_datetime'].timestamp() - query_period_seconds
    end_timestamp = kwargs['interval_start_datetime'].timestamp()
    # select unique device_id and datapoint from table
    devices_datapoints = cratedb.get_unique_deviceid_datapoint(
        table_name=cratedb_source_table,
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp
    )

    for device_id, datapoints in devices_datapoints.items():
        for datapoint in datapoints:
            print(f"Device ID: {device_id}, Datapoint: {datapoint}")

    return devices_datapoints


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
