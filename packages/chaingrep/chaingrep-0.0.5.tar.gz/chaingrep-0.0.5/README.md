# Chaingrep Python Library

The Chaingrep Python library provides convenient access to the Chaingrep API from applications written in Python.

## Documentation
See the [Chaingrep docs](https://docs.chaingrep.com/page/chaingrep-python).

## Installation
You don't need this source code unless you want to modify the package. If you want to use the package, just run:

```
pip install chaingrep
```

Install from source with:
```
python setup.py install
```

## Requirements
- Python 3.6+

## Usage
The library needs to be instantiated with your Chaingrep API key. Here's are a few examples of how the library can be used:

```python
from chaingrep import Chaingrep
from datetime import datetime, timedelta

chaingrep = Chaingrep("<API_KEY>")

# Parse a transaction
transaction = chaingrep.transaction("0xc4fd8359894ad78b04a5cd784106bcf6c413db8372492e744433533abc848ac6").parse()

print(transaction.transaction_type)


# Parse an account's transactions
account_transactions = chaingrep.account("0xa4722f1b4B552951828e6A334C5724b34B19A327").parse_transactions()

for transaction in account_transactions:
    print(transaction.time.timeago)


# Query all interactions between an account and a contract in the past month
target_account = "0xa4722f1b4B552951828e6A334C5724b34B19A327" # Me
target_contract = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48" # USDC

current_datetime = datetime.utcnow()
past_datetime = current_datetime - timedelta(days=30) # One month ago

# Construct the query
query = chaingrep.query()
query.query({
    "account": target_account,
    "contract": target_contract
})
query.timeframe(past_datetime, current_datetime)

# Return a count
interactions_count = query.count()

# Return results
interactions = query.execute()
```

## Handling exceptions
Unsuccessful requests raise exceptions. The class of the exception will reflect the sort of error that occurred, and the error message will provide more context. See [Exceptions](https://github.com/chaingrep/chaingrep-py/blob/main/chaingrep/exceptions.py) for more.

```python
from chaingrep import Chaingrep

chaingrep = Chaingrep("<API_KEY>")

transaction = chaingrep.transaction("not_a_valid_hash").parse()
# InvalidTransactionHashError: <error message>
```
