import unittest
import requests
from server import app
from faker import Faker

class ProcessPaymentTestCase(unittest.TestCase):
    """This class represents the ProcessPayment test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.client = app.test_client
        self.fake = Faker()

        self.payload = {
            'credit_card_number': self.fake.credit_card_number(),
            'card_holder': self.fake.name(),
            'expiration_date': self.fake.date_time_this_decade(before_now=False, after_now=True),
            'security_code': self.fake.credit_card_security_code(),
            'amount': self.fake.pyfloat(positive=True, right_digits=2, max_value=1000),
        }
    
    def test_is_app_running(self):
        response = self.client().get('/server-check')
        self.assertEqual(response.status_code, 200)
        
    def test_is_payment_processed(self):
        response = self.client().post(
            '/process-payment',
            data=self.payload
        )
        self.assertEqual(response.status_code, 200)