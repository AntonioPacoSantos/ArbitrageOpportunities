import math 
import pyRofex as pr
from datetime import date 
import os 


def market_rate_for_future(symbol,current_rate):
    """
    :param symbol: the symbol of the instrument
    :type symbol: str
    :param current_rate: the current rate of interest(13-weeks period)
    :type current_rate: float
    :return: the market rate for the future instrument
    """
    #Get the maturity date of the chosen instrument
    date_of_closing = pr.get_instrument_details(symbol)['instrument']['maturityDate']
    #Get the value of t 
    today = date.today()
    maturity_date = date(int(date_of_closing[0:4]), int(date_of_closing[4:6]), int(date_of_closing[6:8]))
    #The value of t is the distance in days between the current date and the maturity date divided by 91 (13 weeks)
    tValue = (maturity_date - today).days / 91
    return ((1 + current_rate)**tValue)-1
    

def compute_rate(symbol,market_data,spots):
    """
    :param symbol: the symbol of the instrument 
    :type symbol: str
    :param market_data: the bid or the offer for the instrument
    :type market_data: float
    :param spots: the spots for each of the possible instruments 
    :type spots: dict
    :return: the rate of interest implied by the offer or bid for the instrument
    """
    #Get the spot for the chosen instrument 
    spot_price = spots[symbol]
    #Get the maturity date of the chosen instrument
    date_of_closing = pr.get_instrument_details(symbol)['instrument']['maturityDate']
    #Compute the value of t 
    tValue = parse_maturity_date_and_compute_tValue(date_of_closing)
    return math.log(market_data/spot_price) / tValue


def parse_maturity_date_and_compute_tValue(maturity_date): 
    """ 
    :param maturity_date: the maturity date of the instrument
    :type maturity_date: str
    :return: the distance in years between the current date and the maturity date
    """
    current_date = date.today()
    maturity_parsed_date = date(int(maturity_date[0:4]), int(maturity_date[4:6]), int(maturity_date[6:8]))
    tValue = (maturity_parsed_date - current_date).days / 365
    return tValue    


def get_credentials():
    if not os.path.exists('config.txt'):
        config_file = open('config.txt', "w")
        print("No existe el archivo de configuración.")
        user = input('Ingrese su usario:') 
        password = input('Ingrese su contraseña:')
        account = input('Ingrese su cuenta:')
        config_file.write(f"user={user}\n",)
        config_file.write(f"password={password}\n")
        config_file.write(f"account={account}")
        config_file.close()
        credentials = {
            'user': user,
            'password': password,
            'account': account
        }
    else:
        config_file = open('config.txt', "r")
        credentials = {}
        for line in config_file:
            key, value = line.split('=')
            value = value.strip()
            credentials[key] = value
    return credentials
    