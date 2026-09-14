from parameters.standard_deviation import *
from parameters.math_expectation import *

def getVariation(num_series):
    if len(num_series) == 0:
        return None

    standard_deviation = getStandardDeviation(num_series)
    math_expectation = getMathExpectation(num_series)

    variation = (standard_deviation * 100) / math_expectation

    return variation