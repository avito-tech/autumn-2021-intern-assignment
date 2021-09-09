import datetime as dt
import random


def test():
    yers = [
        (year,
         year) for year in range(
            dt.datetime.now().year,
            dt.datetime.now().year +
            5)]
    return yers


print(test())
