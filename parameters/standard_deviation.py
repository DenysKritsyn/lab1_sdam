from parameters.dispersion import *

def getStandardDeviation(num_series):
    if len(num_series) == 0:
        return None

    dispersion = getDispersion(num_series)
    standard_deviation = pow(dispersion, 0.5)
    
    return standard_deviation