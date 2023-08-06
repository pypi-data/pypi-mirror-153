import concurrent.futures

from chaingrep.api_resources.query import Query
from chaingrep.api_resources.requester import Requester
from chaingrep.exceptions import AccountParsingError, InvalidAccountError, InvalidSubscriptionError


class Account:
    def __init__(self, account, auth):
        self.account = account
        self.auth = auth

        account_len = len(account)
        account_prefix = account[0:2]

        if account_len != 42:
            raise InvalidAccountError("Account must have 42 characters.")

        if account_prefix != "0x":
            raise InvalidAccountError("Account must start with '0x'.")

    def parse_transactions(self, start=0):
        start_type = type(start)

        if start_type is int:
            if start > 990:
                raise AccountParsingError("The maximum value for the start parameter is 990 (1000 transactions).")
        elif start_type is str:
            if start != "auto":
                raise AccountParsingError("The 'start' parameter takes an integer or 'auto'.")

        method_endpoint = f"/account/{self.account}/transactions"

        if start_type is int:
            parsed_transactions = Requester(self.auth).get(method_endpoint, params={"start": start})
        elif start_type is str:
            # Count transactions in account
            count_query = Query(self.auth)
            count_query.query({"account": self.account})
            transaction_count = count_query.count()
            transaction_count = transaction_count.get("count")

            parsed_transactions_unordered = []
            pages = [n for n in range(0, transaction_count) if n % 10 == 0]
            req = Requester(self.auth).get
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                future_to_url = (executor.submit(req, method_endpoint, {"start": page}) for page in pages)
                for future in concurrent.futures.as_completed(future_to_url):
                    data = future.result()
                    if data is not None:
                        data = data.get("response", [])
                        for transaction in data:
                            parsed_transactions_unordered.append(transaction)

            parsed_transactions = sorted(
                parsed_transactions_unordered,
                key=lambda transaction: transaction.get("time").get("unix_timestamp"),
                reverse=True,
            )
            parsed_transactions = {"status_code": 200, "response": parsed_transactions}

        status_code = parsed_transactions.get("status_code")
        response = parsed_transactions.get("response")

        if status_code != 200:
            raise AccountParsingError(response)

        return response

    def get_transactions(self, start=0):
        start_type = type(start)

        if start_type is int:
            if start > 99000:
                raise AccountParsingError("The maximum value for the start parameter is 99000 (100000 transactions).")
        elif start_type is str:
            if start != "auto":
                raise AccountParsingError("The 'start' parameter takes an integer or 'auto'.")

        method_endpoint = f"/account/{self.account}/transactions/raw"

        if start_type is int:
            parsed_transactions = Requester(self.auth).get(method_endpoint, params={"start": start})
        elif start_type is str:
            # Count transactions in account
            count_query = Query(self.auth)
            count_query.query({"account": self.account})
            transaction_count = count_query.count()
            transaction_count = transaction_count.get("count")

            parsed_transactions_unordered = []
            pages = [n for n in range(0, transaction_count) if n % 10 == 0]
            req = Requester(self.auth).get
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                future_to_url = (executor.submit(req, method_endpoint, {"start": page}) for page in pages)
                for future in concurrent.futures.as_completed(future_to_url):
                    data = future.result()
                    if data is not None:
                        data = data.get("response", [])
                        for transaction in data:
                            parsed_transactions_unordered.append(transaction)

            parsed_transactions = sorted(
                parsed_transactions_unordered,
                key=lambda transaction: transaction.get("timestamp"),
                reverse=True,
            )
            parsed_transactions = {"status_code": 200, "response": parsed_transactions}

        status_code = parsed_transactions.get("status_code")
        response = parsed_transactions.get("response")

        if status_code != 200:
            raise AccountParsingError(response)

        return response

    def subscribe(self, url):
        method_endpoint = "/subscription"
        payload = {"url": url, "address": self.account}

        subscription = Requester(self.auth).post(method_endpoint, payload)
        status_code = subscription.get("status_code")
        response = subscription.get("response")

        if status_code != 200:
            raise InvalidSubscriptionError(response)

        return response

    def unsubscribe(self, uid):
        method_endpoint = f"/subscription/{uid}"

        subscription = Requester(self.auth).delete(method_endpoint)
        status_code = subscription.get("status_code")
        response = subscription.get("response")

        if status_code != 200:
            raise InvalidSubscriptionError(response)

        return response
