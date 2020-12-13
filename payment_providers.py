import random


class PaymentGateway:
    def __init__(self, amount):
        self.amount = amount
        super().__init__()
    
    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, value):
        self._status = value

    def fetch_gateway_wrt_amount(self):
        if self.amount < 20:
            return CheapPaymentGateway(self.amount)
        elif 20 <= self.amount <= 500:
            return ExpensivePaymentGateway(self.amount)       
        else:
            return PremiumPaymentGateway(self.amount)


class PremiumPaymentGateway(PaymentGateway):
    retry_limit = 0 #Initially zero set.
    
    def __repr__(self):
        return 'Premium Payment Gateway'

    def process_payment(self):
        """ payment is processed successfully and set status"""
        self.status = random.choices([200, 400])[0]
        # self.status = 400 #Bad request
        self.retry_limit_incrementor()

    def retry_limit_incrementor(self):
        self.retry_limit += 1

class ExpensivePaymentGateway(PaymentGateway):
    is_available = random.choices([True, False])[0]
    
    def __repr__(self):
        return 'Expensive Payment Gateway'

    def process_payment(self):
        """ payment is processed successfully and set status to 200 ok"""
        self.status = 200 if self.is_available else 400


class CheapPaymentGateway(PaymentGateway):
    
    def __repr__(self):
        return 'Cheap Payment Gateway'

    def process_payment(self):
        """ payment is processed successfully and set status to 200 ok"""
        self.status = 200