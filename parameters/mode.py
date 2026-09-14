class NoModeError(Exception):
    def __init__(self, message="No mode found in the numerical series"):
        super().__init__(message)


def getMode(num_series):
    if len(num_series) == 0:
        return None

    counts = {}
    for num in num_series:
        counts[num] = counts.get(num, 0) + 1

    max_count = max(counts.values())

    if max_count == 1:
        raise NoModeError()

    modes = []
    for num, count in counts.items():
        if count == max_count:
            modes.append(num)

    return modes
