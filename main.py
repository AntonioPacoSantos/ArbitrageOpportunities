from flask import Flask, jsonify, session 
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from arbitrage_detection import ArbitrageOpportunity
import yfinance as yf 

    
#Getting last interest rates from the treasury bond
treasury_yield = yf.Ticker("^IRX")
history = treasury_yield.history(period="1mo")
latest_rate = float("{:.1f}".format((history['Close'][-1])))
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
#credentials = get_credentials()

app = Flask(__name__)
CORS(app)


api = Api(app) 
ao = {} 
login_put_args = reqparse.RequestParser()
login_put_args.add_argument("user", type=str, help="Username is required", required=True, location='json')
login_put_args.add_argument("password", type=str, help="Password is required", required=True, location = 'json')
login_put_args.add_argument("account", type=str, help="Account is required", required=True, location= 'json')
    
class Arbitrage(Resource):
    def get(self):
        response =  jsonify({'bid': ao['data'].bid_rates, 'offer': ao['data'].offer_rates,'ir': ao['data'].current_rate, 'arbitrage': ao['data'].arbitrage_opportunities})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    
class Login(Resource): 
    def post(self):
        args = login_put_args.parse_args()
        ao['data'] = ArbitrageOpportunity(instruments, spot_for_future, latest_rate, args)
        return {'message': 'Credentials received'}
        
api.add_resource(Arbitrage, '/')
api.add_resource(Login, '/login')
if __name__ == "__main__":
    app.run(debug=True)

  