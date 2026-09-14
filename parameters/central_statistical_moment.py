from parameters.math_expectation import *
from parameters.average import *

def getCentralStatisticalMoment(k, num_series):
    if len(num_series) == 0:
        return None

    average = getAverage(num_series)
    centralStatisticalMoment = getMathExpectation([pow(i-average,k) for i in num_series])

    return centralStatisticalMoment