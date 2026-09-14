from parameters.central_statistical_moment import *
from parameters.standard_deviation import *

def getExcess(num_series):
    if len(num_series) == 0:
        return None

    central_statistical_moment_4 = getCentralStatisticalMoment(4, num_series)
    standard_deviation = getStandardDeviation(num_series)

    excess = (central_statistical_moment_4 / pow(standard_deviation, 4)) - 3

    return excess