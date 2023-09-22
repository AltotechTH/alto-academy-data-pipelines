if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd

# import database utilities
from alto_academy_workshop.utils.database import AltoCrateDB

@data_loader
def load_data(filter_list, *args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
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
    
    cratedb = AltoCrateDB(
        host=cratedb_host,
        port=cratedb_port
    )
    all_df = pd.DataFrame()

    for f in filter_list:
        data = cratedb.query_data(table_name=cratedb_source_table, filters=f)
        df = pd.DataFrame(data)
        if df.empty:
            print(f"Data for device '{list(f['device_id'].values())[0]}' is not found")
            continue
        else:
            print(f"Found {len(df)} entries for the filter {f}")
            all_df = pd.concat([all_df, df], ignore_index=True)  # Concat dataframe

    if not all_df.empty:
        # all_df['timestamp'] = all_df['timestamp'] * 1000
        all_df['timestamp'] = pd.to_datetime(all_df['timestamp'], unit='ms')# .dt.round('1min')
        # all_df['timestamp'].astype('datetime64[s]')
        all_df = all_df.set_index('timestamp')
        all_df = all_df.sort_index(ascending=True)
    else:
        print(f"No data is found for the filters {filter_list}")
        return [filter_list, []]
    
    return [filter_list, all_df]