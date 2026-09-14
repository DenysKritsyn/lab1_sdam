def getAverage(num_series):
    if len(num_series) == 0:
        return None

    sum = 0

    for i in num_series:
        sum+=i

    average = sum/len(num_series)

    return average