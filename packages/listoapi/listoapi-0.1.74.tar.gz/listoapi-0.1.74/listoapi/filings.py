# -*- coding: utf-8 -*-
from .api import ListoAPI, WrongDataFormat


class Filings(ListoAPI):
    def __init__(self, token, base_url):
        super(Filings, self).__init__(token, base_url)

    def get_filings_rfcs(self):
        """List all rfcs the token has access to"""
        return self.make_request(method="GET", path="/filings/rfcs/").json()

    def get_filings_rfcs_status(self, rfc_id):
        try:
            assert (type(rfc_id) is int), 'El campo `rfc_id` debe ser tipo `int`'
            return self.make_request(method="GET", path="/filings/rfcs/" + str(rfc_id) + "/status") \
                .json()
        except WrongDataFormat:
            pass

    def get_filings_periods(self, filing_period_id):
        try:
            assert (type(filing_period_id)
                    is int), 'El campo `filing_period_id` debe ser tipo `int`'
            return self.make_request(method="GET", path="/filings/filing_periods/" + str(filing_period_id)) \
                .json()
        except WrongDataFormat:
            pass

    def get_filings_filing(self, filing_id):
        try:
            assert (type(filing_id)
                    is int), 'El campo `filing_id` debe ser tipo `int`'
            return self.make_request(method="GET", path="/filings/filings/" + str(filing_id)) \
                .json()
        except WrongDataFormat:
            pass

    def get_filings_get_legal_address(self, rfc_id):
        try:
            assert (type(rfc_id) is int), 'El campo `rfc_id` debe ser tipo `int`'
            return self.make_request(method="GET", path="/filings/get_legal_address/" + str(rfc_id)) \
                .json()
        except WrongDataFormat:
            pass

    def get_filings_creditbalances(self, credit_balance_id):
        try:
            assert (type(credit_balance_id) is int), 'El campo `credit_balance_id` debe ser tipo `int`'
            return self.make_request(method="GET", path="/filings/creditbalances/" + str(credit_balance_id)) \
                .json()
        except WrongDataFormat:
            pass
    
    def get_filings_rfcs_detalle(self, rfc_id):
        try:
            assert (type(rfc_id) is int), 'El campo `rfc_id` debe ser tipo `int`'
            return self.make_request(method="GET", path="/filings/rfcs/" + str(rfc_id)) \
                .json()
        except WrongDataFormat:
            pass

    def get_filings_credit_balance_accreditations(self, credit_balance_id):
        try:
            assert (type(credit_balance_id) is int), 'El campo `credit_balance_id` debe ser tipo `int`'
            return self.make_request(method="GET", path="/filings/credit_balance_accreditations/" + str(credit_balance_id)) \
                .json()
        except WrongDataFormat:
            pass

    def get_filings_credit_balance_reductions(self, filing_id, tax_type, credit_balance_type):
        try:
            assert (type(filing_id) is int), 'El campo `filing_id` debe ser tipo `int`'
            assert (type(tax_type) is str), 'El campo `tax_type` debe ser tipo `str`'
            assert (type(credit_balance_type) is str), 'El campo `credit_balance_type` debe ser tipo `str`'
            return self.make_request(method="GET", path="/filings/credit_balance_reductions/" + str(filing_id) + "/" + tax_type + "/" + credit_balance_type) \
                .json()
        except WrongDataFormat:
            pass

    def get_filings_rfcs_taxes(self, rfc_id):
        try:
            assert (type(rfc_id) is int), 'El campo `rfc_id` debe ser tipo `int`'
            return self.make_request(method="GET", path="/filings/rfcs/" + str(rfc_id) + "/taxes") \
                .json()
        except WrongDataFormat:
            pass

    def get_filings_rfcs_credit_balance_originations(self, rfc_id):
        try:
            assert (type(rfc_id) is int), 'El campo `rfc_id` debe ser tipo `int`'
            return self.make_request(method="GET", path="/filings/rfcs/" + str(rfc_id) + "/credit_balance_originations") \
                .json()
        except WrongDataFormat:
            pass
        
