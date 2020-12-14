import unittest
from faker import Faker
from payment_providers import PremiumPaymentGateway, ExpensivePaymentGateway, CheapPaymentGateway
from payment_providers import PaymentGateway

class PaymentGatewayTestCase(unittest.TestCase):
    """This class represents the PaymentGateway test case"""

    def setUp(self):
        self.fake = Faker()
        self.amount1 = self.fake.pyfloat(positive=True, right_digits=2, min_value=1, max_value=20)
        self.amount2 = self.fake.pyfloat(positive=True, right_digits=2, min_value=21, max_value=500)
        self.amount3 = self.fake.pyfloat(positive=True, right_digits=2, min_value=501, max_value=1000)

    def test_payment_gateways_selection_wrt_amount(self):
        if self.amount1 < 20:
            cheap_gateway = CheapPaymentGateway(amount=self.amount1)
            self.assertEqual(str(cheap_gateway), 'Cheap Payment Gateway', 'Required gateway not selected')

        if 20 <= self.amount2 <= 500:
            expensive_gateway = ExpensivePaymentGateway(amount=self.amount2)
            self.assertEqual(str(expensive_gateway), 'Expensive Payment Gateway', 'Required gateway not selected')

        if self.amount3 > 500:
            premium_gateway = PremiumPaymentGateway(amount=self.amount2)
            self.assertEqual(str(premium_gateway), 'Premium Payment Gateway', 'Required gateway not selected')

    def test_get_gateway_wrt_amount(self):
        driver = PaymentGateway(self.amount2)
        payment_gateway = driver.fetch_gateway_wrt_amount()
        self.assertEqual(str(payment_gateway), 'Expensive Payment Gateway', 'Required gateway not returned')
    
    def test_expensive_payment_gateway_service(self):
        amount_tobe_paid = self.amount2 #Between £21-500
        payment_gateway = ExpensivePaymentGateway(amount_tobe_paid)
        
        if payment_gateway.is_available:
            payment_gateway.process_payment()
            self.assertEqual(payment_gateway.status, 200, '400 bad request')
        else:
            cheap_gateway = CheapPaymentGateway(amount_tobe_paid)
            cheap_gateway.process_payment()
            self.assertEqual(cheap_gateway.status, 200, '400 bad request')
    
    def test_cheap_payment_gateway_service(self):
        amount_tobe_paid = self.amount1 #Less than £20
        payment_gateway = CheapPaymentGateway(amount_tobe_paid)
        payment_gateway.process_payment()
        self.assertEqual(payment_gateway.status, 200, '400 bad request')
    
    def test_premium_payment_gateway_service(self):
        amount_tobe_paid = self.amount3 #greater than £500
        payment_gateway = PremiumPaymentGateway(amount_tobe_paid)
        payment_gateway.process_payment()
        
        if payment_gateway.status != 200:
            """Retrying up to 3 times in case payment does not get processed."""
            while payment_gateway.retry_limit <= 3:
                payment_gateway.process_payment()
                if payment_gateway.status == 200:
                    self.assertEqual(payment_gateway.status, 200, '400 bad request')
                    break
            else:
                self.assertEqual(payment_gateway.status, 200, '400 bad request')
        else:
            self.assertNotEqual(payment_gateway.retry_limit, 4, 'Invalid retry limit')




