from flask import Flask, jsonify
from flask_restful import Api, Resource 
from flask_cors import CORS
from arbitrage_detection import ArbitrageOpportunity
import yfinance as yf 
from utils import get_credentials

    
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

ao = ArbitrageOpportunity(instruments, spot_for_future, latest_rate,credentials)

    
app = Flask(__name__)
CORS(app)

api = Api(app)

@app.route('/', methods=['GET'])
def get_dictioanry():
    response =  jsonify({'bid': ao.bid_rates, 'offer': ao.offer_rates,'ir': latest_rate })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    app.run(debug=True)
  