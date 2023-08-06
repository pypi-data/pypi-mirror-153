# -*- coding: utf-8 -*-
from time import sleep
from .api import ListoAPI, TooManyRequests


class Payments(ListoAPI):
    def __init__(self, token, base_url):
        super(Payments, self).__init__(token, base_url)

    def search(self, sleep_length=30, **kwargs):
        """
        kwargs:
            - effective_on (str): ISO 8601 datetime range (r:YYYY-MM-DDTHH:mm:ss_YYYY-MM-DDTHH:mm:ss)
            - group_id (str|int): Identifier to group invoices by payment
            - invoice_type (str: 'incomes'|'expenses'): Type of invoices linked to payments
        """
        def _request(kwargs):
            return self.make_request(
                method="GET", path="/payments/list/",
                params=kwargs)

        kwargs.setdefault("offset", 0)
        size = kwargs.setdefault("size", 250)

        while True:
            try:
                r = _request(kwargs)
            except TooManyRequests:
                sleep(sleep_length)
                r = _request(kwargs)
            r = r.json()
            if not r:
                break
            for p in r:
                yield p
            kwargs["offset"] += size
