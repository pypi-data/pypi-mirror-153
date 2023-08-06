# -*- coding: utf-8 -*-
from .api import ListoAPI, WrongDataFormat


class Reports(ListoAPI):
    def __init__(self, token, base_url):
        super(Reports, self).__init__(token, base_url)

    def get_reports_income_statement(self, rfc_id):
        try:
            assert (type(rfc_id) is int), 'El campo `rfc_id` debe ser tipo `int`'
            return self.make_request(method="GET", path="/reports/income_statement/" + str(rfc_id) + "/json") \
                .json()
        except WrongDataFormat:
            pass

    def get_reports_balance_sheet(self, rfc_id):
        try:
            assert (type(rfc_id) is int), 'El campo `rfc_id` debe ser tipo `int`'
            return self.make_request(method="GET", path="/reports/balance_sheet/" + str(rfc_id) + "/json") \
                .json()
        except WrongDataFormat:
            pass
