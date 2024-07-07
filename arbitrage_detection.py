import pyRofex as pr  
import yfinance as yf
from utils import compute_rate



class ArbitrageOpportunity: 
    def __init__(self, instruments, spots,current_rate): 
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
        pr.initialize(user="antoniopacosantos11540",
                   password="dggybB0#",
                   account="REM11540",
                   environment=pr.Environment.REMARKET)
        
        pr.init_websocket_connection(market_data_handler=self.market_data_handler,
                                  error_handler=self.error_handler,
                                  exception_handler=self.exception_handler)
        pr.market_data_subscription(tickers=self.instruments,entries=self.entries)
        
        
    def market_data_handler(self,message):
        print("Market Data Message Received: {0}".format(message))
        #Check the bid and the offer of the updated instrument 
        bid = message['marketData']['BI']
        offer = message['marketData']['OF']            
        #First case: bid was updated and new lending rate has to be computed 
        if bid is not None and bid != []:
            #Get the symbol of the instrument that was updated and the new bid price 
            symbol = message['instrumentId']['symbol']
            bid_price = bid[0]['price']
            rate = compute_rate(symbol,bid_price,self.spot)
            self.bid_rates[symbol] = rate
            if rate > self.current_rate:
                print(f"La tasa de interés implícita tomadora de {symbol} es mayor a la tasa de interés del bono del Tesoro a 10 años más reciente. Oportunidad de arbitraje")
    
        #Second case: offer was updated and new borrowing rate has to be computed
        if offer is not None and offer != []: 
            #Get the symbol of the instrument that was updated and the new offer price
            symbol = message['instrumentId']['symbol']
            offer_price = offer[0]['price']
            rate = compute_rate(symbol,offer_price,self.spot)
            self.offer_rates[symbol] = rate
            if rate < self.current_rate:
                print(f"La tasa de interés implícita colocadora de {symbol} es menor a la tasa de interés del bono del Tesoro a 10 años más reciente. Oportunidad de arbitraje")
    
    
    def error_handler(self,message):
        print("Error Message Received: {0}".format(message))


    def exception_handler(self,e):
        print("Exception Occurred: {0}".format(e))
        
        

if __name__ == "__main__":
    
    #Getting current interest rates from the treasury bond
    treasury_yield = yf.Ticker("^TNX")
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
    tickers = yf.Tickers("ggal pamp.ba ypf ARS=X")
    
    #Missing spot for usd 
    spot_ggal = (tickers.tickers['GGAL'].info)['currentPrice']
    spot_pamp = (tickers.tickers['PAMP.BA'].info)['currentPrice']
    spot_ypfd = (tickers.tickers['YPF'].info)['currentPrice']
    spot_usd = (tickers.tickers['ARS=X'].info)['previousClose']
    
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
    
    ArbitrageOpportunity(instruments, spot_for_future, latest_rate)
