def getScope(num_series):
    series_len = len(num_series)

    if series_len == 0:
        return None

    min_val = min(num_series)
    max_val = max(num_series)

    scope = max_val - min_val


    return scope