if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(devices_datapoints, *args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    query_period_seconds = kwargs.get("query_period_seconds", 60)
    if isinstance(query_period_seconds, str):
        query_period_seconds = int(query_period_seconds)
    # construct filter
    start_timestamp = kwargs['interval_start_datetime'].timestamp() - query_period_seconds
    end_timestamp = kwargs['interval_start_datetime'].timestamp()
    
    # end_timestamp = 1693045380
    # start_timestamp = end_timestamp - query_period_seconds

    filter_list = []
    for device_id, datapoints in devices_datapoints.items():
        filters = {
            'device_id': {'=': device_id},
            'datapoint': {'IN': datapoints},
            'timestamp': {'>=': int(start_timestamp) * 1000, '<': int(end_timestamp) * 1000},  # Times 1000 to be in ms uni
        }
        filter_list.append(filters)

    return filter_list