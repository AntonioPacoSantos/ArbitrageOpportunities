import math 


def compute_lending_rate(price,spot, tValue):
    return math.log(price/spot) / tValue
