from flask import Flask, Response, abort  
from flask_restful import Resource, Api, reqparse, inputs
from payment_providers import PaymentGateway
from datetime import datetime

app = Flask(__name__)   
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('task')

class ServerHealthCheck(Resource):
    def get(self):
        return '<h1>Server is Up and Running</h1>'

class ProcessPayment(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('credit_card_number', type=str, help='A valid credit card number', required=True)
        self.reqparse.add_argument('card_holder', type=str, help='Credit Card holder name', required=True)
        self.reqparse.add_argument('expiration_date', type=lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S'), help='Expiration Date', required=True)
        self.reqparse.add_argument('security_code', type=str, help='Security Code(3 digits)')
        self.reqparse.add_argument('amount', type=float, help='Positve Amount', required=True)
        
        super(ProcessPayment, self).__init__()

    def get(self):
        return {'hello': 'world'}
    
    def post(self):
        # print("data: ", self.reqparse.parse_args() )
        request = self.reqparse.parse_args()
        amonut_paid = request.get('amount')

        try:
            pay_gateway = PaymentGateway(amonut_paid)
            gateway = pay_gateway.fetch_gateway_wrt_amount()
            gateway.process_payment()
            if gateway.status:
                return Response({}, status=gateway.status)
        
        except Exception:
            return abort(500) #Internal server error 
        

api.add_resource(ServerHealthCheck, '/server-check')
api.add_resource(ProcessPayment, '/process-payment')

if __name__ =='__main__':  
    app.run(debug = True)  