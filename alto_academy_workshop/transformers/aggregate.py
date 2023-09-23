if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pendulum

def seconds_to_duration(seconds):
    """
    Convert seconds (numeric) to duration string. Round to the nearest minute or hour.
    """
    if seconds < 60:
        return f"{seconds}sec"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes}min"
    else:
        hours = seconds // 3600
        return f"{hours}h"

@transformer
def transform(data2transform, *args, **kwargs):
    """
    Aggregate the raw data.
    """
    timescaledb_destination_table = kwargs.get("timescaledb_destination_table", "aggregated_data")
    resample_seconds = kwargs.get("resample_seconds", 60)
    resample_period = seconds_to_duration(resample_seconds)
    query_period_seconds = kwargs.get("query_period_seconds", 60)
    expected_num_of_data_per_point = int(query_period_seconds) // int(resample_seconds)

    filter_list, all_df = data2transform[0], data2transform[1]

    agg_data = list()
    
    if isinstance(all_df, list) and all_df == []:
        print("There is no raw data for all devices to aggregate.")
        return agg_data, timescaledb_destination_table

    for f in filter_list:
        device_id = list(f['device_id'].values())[0]
        datapoints = list(f['datapoint'].values())[0]
        
        print("="*20)
        print(f"Device: {device_id}")

        if device_id in all_df.values:
            for datapoint in datapoints:
                aggregate_funcs = ["mean", "first", "last", "mode", "max", "sum"]
                data = all_df[all_df["datapoint"] == datapoint]
                data = data[data["device_id"] == device_id]
                series = data["value"]
                
                if data.empty:
                    print(f"'{datapoint}' has no data")
                    continue
                else:
                    try:
                        series = series.astype(float)
                        aggregate_funcs = ["mean"]
                    except Exception:
                        aggregate_funcs = ["mode"]
                        print(f"Failed to convert {datapoint} to float.")
                for agg_func in aggregate_funcs:
                    aggregation_type = f"{agg_func}_{resample_period}"
                    if agg_func == "mean":
                        agg_series = series.resample(resample_period).mean()
                    elif agg_func == "first":
                        agg_series = series.resample(resample_period).first()
                    elif agg_func == "last":
                        agg_series = series.resample(resample_period).last()
                    elif agg_func == "mode":
                        agg_series = series.resample(resample_period).apply(lambda x: x.mode())
                    elif agg_func == "max":
                        agg_series = series.resample(resample_period).max()
                    elif agg_func == "sum":
                        agg_series = series.resample(resample_period).sum()
                    else:
                        print(f"Unknown aggregation function: {agg_func} for device_id: {device_id}")
                        continue
                    
                    print(f"{len(agg_series)}/{expected_num_of_data_per_point} data points found for '{datapoint}' for device '{device_id}' using '{agg_func}' functions")

                    for idx, v in agg_series.items():
                        if agg_series.dtype != 'object':
                            v = round(v, 4)
                        ts = idx.timestamp()
                        agg_data.append({
                            "timestamp": pendulum.from_timestamp(ts, tz="Asia/Bangkok"),
                            "device_id": device_id,
                            "aggregation_type": aggregation_type,
                            "datapoint": datapoint,
                            "value": v,
                        })
        else:
            print("There is no data for Device:", device_id)

    return agg_data, timescaledb_destination_table