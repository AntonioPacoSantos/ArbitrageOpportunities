import math 


def compute_rate(price,spot, tValue):
    return math.log(price/spot) / tValue
