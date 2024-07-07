import math 
import pyRofex as pr
from datetime import date 


def compute_rate(symbol,bid_price,spots):
    spot_price = spots[symbol]
    date_of_closing = pr.get_instrument_details(symbol)['instrument']['maturityDate']
    tValue = parse_maturity_date_and_compute_tValue(date_of_closing)
    return math.log(bid_price/spot_price) / tValue


def parse_maturity_date_and_compute_tValue(maturity_date): 
    current_date = date.today()
    maturity_parsed_date = date(int(maturity_date[0:4]), int(maturity_date[4:6]), int(maturity_date[6:8]))
    tValue = (maturity_parsed_date - current_date).days / 365
    return tValue    