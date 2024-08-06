import unittest
from applications.web.app import get_gainer_data
from components.DatabaseGateway import DatabaseGateway
from unittest.mock import patch

class TestWebApGetReportData(unittest.TestCase):

    MOCKDATA = "[{'ticker': 'NOVVW', 'price': '0.0447', 'change_amount': '0.0297', 'change_percentage': '198.0%', 'volume': '24200'}]"

    def setUp(self):
        self.mockdata = "[{'ticker': 'NOVVW', 'price': '0.0447', 'change_amount': '0.0297', 'change_percentage': '198.0%', 'volume': '24200'}]"

    '''
    Test the add_data function.
    '''
    @patch.object(DatabaseGateway, 'get_data', return_value=MOCKDATA)
    def test_get_gainer_data(self, mock_get_data):
        #gateway = DatabaseGateway()
        result = get_gainer_data()
        self.assertEqual(result, self.mockdata)
        mock_get_data.assert_called_once()

if __name__ == '__main__':
    unittest.main()
