import random
import datetime as dt


def test():
    yers = [(year, year) for year in range(dt.datetime.now().year, dt.datetime.now().year + 5)]
    return yers

print(test())