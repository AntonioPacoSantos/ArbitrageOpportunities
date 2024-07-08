import unittest 
import pyRofex as pr
from utils import compute_rate, get_credentials

class TestComputeRate(unittest.TestCase): 
    def __init__(self, *args, **kwargs):
        super(TestComputeRate, self).__init__(*args, **kwargs)
        #Initialize environment 
        credentials = get_credentials()
        pr.initialize(user=credentials['user'],
            password=credentials['password'],
            account=credentials['account'],
            environment=pr.Environment.REMARKET)
        
        self.spots = {
            'GGAL/OCT24': 10
        }
        self.symbol = 'GGAL/OCT24'
        self.bid_price = 15
        
    def test_compute_rate(self): 
        self.assertEqual(compute_rate(self.symbol,self.bid_price,self.spots), 1.286910995299826)
        

if __name__ == '__main__':
    unittest.main()

