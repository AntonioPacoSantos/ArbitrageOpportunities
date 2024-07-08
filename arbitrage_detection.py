import pyRofex as pr  
import yfinance as yf
from utils import compute_rate, get_credentials
        
class ArbitrageOpportunity: 
    def __init__(self, instruments, spots,current_rate,credentials): 
        #initialize the class with the instruments, the spots for each instrument, and the current rate of interest for the treasury bond
        self.instruments = instruments
        self.spots = spots
        self.bid_rates = {}
        self.offer_rates = {}
        self.entries = [
            pr.MarketDataEntry.BIDS,
            pr.MarketDataEntry.OFFERS,
        ]
        self.current_rate = current_rate
        
        #initialize the environment and subscribe to the market data
        pr.initialize(user=credentials['user'],
                   password=credentials['password'],
                   account=credentials['account'],
                   environment=pr.Environment.REMARKET)
        
        pr.init_websocket_connection(market_data_handler=self.market_data_handler)
                                  #error_handler=self.error_handler,
                                  #exception_handler=self.exception_handler)
        pr.market_data_subscription(tickers=self.instruments,entries=self.entries)
        
        
    def market_data_handler(self,message):
        """ 
        :param message: the message received from the market data
        :type message: dict
        
        :return: the function updates the interest rates of the instruments, if necessary, and finds arbitrage opportunities
        """
        print("Market Data Message Received: {0}".format(message))
        #Check the bid and the offer of the updated instrument 
        symbol = message['instrumentId']['symbol']
        bid = message['marketData']['BI']
        offer = message['marketData']['OF']            
        #First case: bid was updated and new lending rate has to be computed 
        if bid is not None and bid != []:
            #Get the symbol of the instrument that was updated and the new bid price 
            bid_price = bid[0]['price']
            rate = compute_rate(symbol,bid_price,self.spots)
            #Check if the new bid is higher than the previous bid
            if (symbol in self.bid_rates and rate > self.bid_rates[symbol]) or symbol not in self.bid_rates:
                self.bid_rates[symbol] = rate
                print(f'Nueva tasa de interés implícita tomadora para {symbol}: {rate}')
                if rate > self.current_rate:
                    print(f"La tasa de interés implícita tomadora de {symbol} es mayor a la tasa de interés de mercados. Oportunidad de arbitraje")

        #Second case: offer was updated and new borrowing rate has to be computed
        if offer is not None and offer != []: 
            #Get the symbol of the instrument that was updated and the new offer price   
            offer_price = offer[0]['price']
            rate = compute_rate(symbol,offer_price,self.spots)
            #Check if the new offer is lower than the previous offer
            if (symbol in self.offer_rates and rate < self.offer_rates[symbol]) or symbol not in self.offer_rates:    
                self.offer_rates[symbol] = rate
                print(f'Nueva tasa de interés implícita colocadora para {symbol}: {rate}')
                if rate < self.current_rate:
                    print(f"La tasa de interés implícita colocadora de {symbol} es menor a la tasa de interés de mercado. Oportunidad de arbitraje")
            
        if symbol in self.bid_rates and symbol in self.offer_rates: 
            if self.bid_rates[symbol] > self.offer_rates[symbol]:
                print(f"La tasa de interés implícita tomadora de {symbol} es menor a la tasa de interés implícita colocadora. Oportunidad de arbitraje")
                
    def error_handler(self,message):
        print("Error Message Received: {0}".format(message))


    def exception_handler(self,e):
        print("Exception Occurred: {0}".format(e))
        
        

if __name__ == "__main__":
    
    #Getting last interest rates from the treasury bond
    treasury_yield = yf.Ticker("^IRX")
    history = treasury_yield.history(period="1mo")
    latest_rate = (history['Close'][-1])/100
    #Selecting the instruments to be analyzed
    instruments = [
    'GGAL/OCT24', 
    'GGAL/AGO24',
    'GGAL/AGO24/OCT24', 
    'PAMP/OCT24',
    'PAMP/AGO24',
    'PAMP/AGO24/OCT24',
    'YPFD/OCT24',
    'YPFD/AGO24',
    'YPFD/AGO24/OCT24',
    'DLR/AGO24'
    ]   


    #Getting the spots for the chosen instruments
    tickers = yf.Tickers("ggal.ba pamp.ba ypfd.ba ypf")
    
    #Missing spot for usd 
    spot_ggal = (tickers.tickers['GGAL.BA'].info)['currentPrice']
    spot_pamp = (tickers.tickers['PAMP.BA'].info)['currentPrice']
    spot_ypfd = (tickers.tickers['YPFD.BA'].info)['currentPrice']
    
    #Computting CCL for USD with YPF and YPFD.BA
    spot_usd = spot_ypfd/(tickers.tickers['YPF'].info)['currentPrice']
    
    spot_for_future = {
        'GGAL/OCT24': spot_ggal,
        'GGAL/AGO24': spot_ggal,
        'GGAL/AGO24/OCT24': spot_ggal,
        'PAMP/OCT24': spot_pamp,
        'PAMP/AGO24': spot_pamp,
        'PAMP/AGO24/OCT24': spot_pamp,
        'YPFD/OCT24': spot_ypfd,
        'YPFD/AGO24': spot_ypfd,
        'YPFD/AGO24/OCT24': spot_ypfd,
        'DLR/AGO24': spot_usd
    }
    
    #Create a file config with the credentials if not created yet 
    credentials = get_credentials()
    
    ArbitrageOpportunity(instruments, spot_for_future, latest_rate,credentials)
