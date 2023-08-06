# -*- coding: utf-8 -*-
from .api import ListoAPI


class ExchangeRate(ListoAPI):
    def __init__(self, token, base_url):
        super(ExchangeRate, self).__init__(token, base_url)

    def daily(self, currency, date_string):
        """Check exchange rate for specific date and currency

        Args:
        - currency: 3 chars length currency (i.e. USD, EUR, etc...)
        - date_string: YYYY-MM-DD format
        """
        return self.make_request(
            method="GET", path="/fx/daily/%s/%s" % (currency, date_string)).json()

    def invoice(self, currency, date_string):
        """Check exchange rate for specific date and currency

        Args:
        - currency: 3 chars length currency (i.e. USD, EUR, etc...)
        - date_string: YYYY-MM-DD format
        """
        return self.make_request(
            method="GET", path="/fx/invoice/%s/%s" % (currency, date_string)).json()
