# -*- coding: utf-8 -*-
from .api import ListoAPI


class Expenses(ListoAPI):
    def __init__(self, token, base_url):
        super(Expenses, self).__init__(token, base_url)

    def _validate_date_filters(self, kwargs):
        for d in ["dt", "paid_on", "created_on"]:
            if kwargs.get(d):
                self.validate_date_filter(kwargs.get(d))

    def get_accounts(self, **kwargs):
        """Expenses Accounts

        """
        r = self.make_request(
            method="GET", path="/expenses/expense_accounts/",
            params=kwargs).json()["hits"]
        for i in r:
            yield i

    def get_reimbursements(self, **kwargs):
        """Expenses Reimbursements
            - expense_account_alias (str)
            - paid_on (str): ISO 8601 datetime (YYYY-MM-DDTHH:mm:ss)
            - created_on (str): ISO 8601 datetime (YYYY-MM-DDTHH:mm:ss)
            - state (str): status
        """
        # Validate date filters
        self._validate_date_filters(kwargs)

        kwargs.setdefault("offset", 0)
        size = kwargs.setdefault("size", 100)
        while True:
            r = self.make_request(
                method="GET", path="/expenses/reimbursements/",
                params=kwargs).json()["hits"]
            if not r:
                break
            for i in r:
                yield i
            kwargs["offset"] += size

    def get_expenses(self, **kwargs):
        """Expenses Expenses
            - state (str): "data_needed, pending, done"
            - dt (str): ISO 8601 datetime (YYYY-MM-DDTHH:mm:ss)
            - counterparty_rfc (str): counter party RFC
            - expense_account_alias (str)
        """

        # Validate date filters
        self._validate_date_filters(kwargs)

        kwargs.setdefault("offset", 0)
        size = kwargs.setdefault("size", 100)
        while True:
            r = self.make_request(
                method="GET", path="/expenses/expenses/",
                params=kwargs).json()["hits"]
            if not r:
                break
            for i in r:
                yield i
            kwargs["offset"] += size
