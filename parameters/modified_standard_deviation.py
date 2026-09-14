from parameters.modified_dispersion import *

def getModifiedStandardDeviation(num_series):
    if len(num_series) <= 1:
        return None

    modified_dispersion = getModifiedDispersion(num_series)
    modified_standard_deviation = pow(modified_dispersion, 0.5)
    
    return modified_standard_deviation