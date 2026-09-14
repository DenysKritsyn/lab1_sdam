from parameters.central_statistical_moment import *
from parameters.standard_deviation import *

def getAsymmetry(num_series):
    if len(num_series) == 0:
        return None

    central_statistical_moment_3 = getCentralStatisticalMoment(3, num_series)
    standard_deviation = getStandardDeviation(num_series)

    asymmetry = central_statistical_moment_3 / pow(standard_deviation, 3)

    return asymmetry