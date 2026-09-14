def getMathExpectation(num_series):
    series_len = len(num_series)

    if series_len == 0:
        return None
 
    unique_series=set(num_series)
    math_expectation=0

    for i in unique_series:
        math_expectation += i * (num_series.count(i) / series_len)

    return math_expectation