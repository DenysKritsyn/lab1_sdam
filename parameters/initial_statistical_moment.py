from parameters.math_expectation import *

def getInitialStatisticalMoment(k, num_series):
    if len(num_series) == 0:
        return None

    initialStatisticalMoment = getMathExpectation([pow(i,k) for i in num_series])

    return initialStatisticalMoment