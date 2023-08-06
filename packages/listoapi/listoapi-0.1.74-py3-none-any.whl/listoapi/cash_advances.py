# -*- coding: utf-8 -*-
from .api import ListoAPI


class CashAdvances(ListoAPI):
    def __init__(self, token, base_url):
        super(CashAdvances, self).__init__(token, base_url)

    def _validate_date_filters(self, kwargs):
        for d in ["created_on", "paid_on"]:
            if kwargs.get(d):
                self.validate_date_filter(kwargs.get(d))

    def get_cash_advances(self, **kwargs):
        """CASH_ADVANCES
        kwargs:
            - paid_on (str): ISO 8601 datetime (YYYY-MM-DDTHH:mm:ss)
            - created_on (str): ISO 8601 datetime (YYYY-MM-DDTHH:mm:ss)
            - state (str): "available"
            - expense_account_alias (str)
        """
        # Validate date filters
        self._validate_date_filters(kwargs)

        kwargs.setdefault("offset", 0)
        size = kwargs.setdefault("size", 100)
        while True:
            r = self.make_request(
                method="GET", path="/expenses/cash_advances/",
                params=kwargs).json()["hits"]
            if not r:
                break
            for i in r:
                yield i
            kwargs["offset"] += size
