from decimal import Decimal
import unittest

from fastapi.testclient import TestClient

from main import app
from storage.in_memory_store import retrieve_transactions, clear_storage

client = TestClient(app)

class TestAddTransactions(unittest.TestCase):

    def test_happy_path(self):
        
        clear_storage()

        # Post a simple two-line csv payload.
        files = {'data': two_line_csv_file}
        
        response = client.post("/transactions",files=files)
        
        # Check response is what is expected.
        self.assertEqual(201, response.status_code)
        obj = response.json()
        self.assertEqual(len(obj), 2)
        second_one = obj[1]
        self.assertEqual(second_one['amount'], '40.00')
        self.assertEqual(second_one['date'], '2020-07-04')
        self.assertEqual(second_one['category'], 'Income')
        self.assertEqual(second_one['memo'], '347 Woodrow')
        
        # Check the transactions got stored.
        stored = retrieve_transactions()
        self.assertEqual(stored[1].amount, Decimal('40.00'))
        
    def test_one_example_error_path(self):
        
        clear_storage()

        # Post a malformed csv payload.
        files = {'data': "this is malformed csv"}
        response = client.post("/transactions",files=files)
        
        # Check response is what is expected.
        self.assertEqual(400, response.status_code)
        obj = response.json()
        detail = obj['detail']
        self.assertEqual(detail, 'Should be 4 fields, not 1 (this is malformed csv)')
        
class TestReportEndPoint(unittest.TestCase):

    def test_happy_path(self):
        
        clear_storage()

        # First put in some transactions
        files = {'data': two_line_csv_file}
        response = client.post("/transactions",files=files)
        self.assertEqual(201, response.status_code)
        
        # Now request the report
        response = client.get("/report")
        
        # Check response is what is expected.
        self.assertEqual(200, response.status_code)
        obj = response.json()
        self.assertEqual(
            obj,
            {'gross_revenue': '40.00', 'expenses': '18.77', 'net_revenue': '21.23'})
        
        
    def test_an_example_error(self):
        
        clear_storage()
        
        # Now request the report
        response = client.get("/report")
        
        # Check response is what is expected.
        self.assertEqual(400, response.status_code)
        obj = response.json()
        detail = obj['detail']
        expected = 'Cannot generate report because there are no stored transactions - use the /transactions endpoint to put some in.'
        self.assertEqual(detail,expected)
        
        
        
two_line_csv_file = """
    2020-07-01, Expense, 18.77, Fuel§
    2020-07-04, Income, 40.00, 347 Woodrow
"""

if __name__ == '__main__':
    unittest.main()