from parameters.math_expectation import *

def getDispersion(num_series):
    series_len = len(num_series)

    if series_len == 0:
        return None

    math_expectation_squared=pow(getMathExpectation(num_series),2)
    math_expectation_of_squared = getMathExpectation([i*i for i in num_series])

    dispersion=math_expectation_of_squared-math_expectation_squared

    return dispersion