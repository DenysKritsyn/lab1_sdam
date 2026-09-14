from parameters.dispersion import *

def getModifiedDispersion(num_series):
    series_len = len(num_series)

    if series_len <= 1:
        return None

    dispersion=getDispersion(num_series)
    modified_dispersion=series_len*dispersion/(series_len-1)

    return modified_dispersion