def getMedian(num_series):
    series_len = len(num_series)

    if series_len == 0:
        return None

    sorted_series=sorted(num_series)
    median=None
    
    if series_len % 2 == 1:
        median = sorted_series[series_len // 2]
    else:
        median = (sorted_series[series_len // 2] + sorted_series[(series_len // 2) - 1]) / 2

    return median