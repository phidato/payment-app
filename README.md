# Payment App

It is a Flask app for dealing with different payment gateways.

## Run Flask Server

Use the command to run flask server after setting up virtual environment.

```bash
python server.py
```

## Run Test Cases

```python
python -m unittest tests/test_payment_providers.py
python -m unittest tests/test_process_payment.py
