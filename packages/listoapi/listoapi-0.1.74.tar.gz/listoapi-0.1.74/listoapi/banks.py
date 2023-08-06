# -*- coding: utf-8 -*-
from time import sleep
from .api import ListoAPI, TooManyRequests, WrongDataFormat


class Banks(ListoAPI):
    def __init__(self, token, base_url):
        super(Banks, self).__init__(token, base_url)

    def get_bank_accounts(self):
        return self.make_request(method="GET", path="/banks/bank_transaction/facets") \
            .json()['facets']['bank_account']

    def upload_bank_files(self, filename, file_stream, rfc_id, bank=None, account_number=None):
        print('Uploading file:', filename)
        try:

            assert type(filename) is str and len(filename) > 3, 'El nombre del archivo debe ser cadena de texto válida'
            assert type(rfc_id) is int, 'El campo `rfc_id` debe ser tipo `int`'

            assert type(account_number) is str if account_number is not None else True, 'El campo `account_number` debe ser tipo `string`'
            assert len(account_number) > 4 if account_number is not None else True, 'El campo `account_number` debe ser una cadena de texto válida'

            assert type(bank) is str if bank is not None else True, 'El campo `bank` debe ser tipo `string`'
            assert len(bank) > 2 if bank is not None else True, 'El campo `bank` debe ser una cadena de texto válida'

            return self.make_request(method="POST", path="/banks/upload_bank_files/sync",
                                    files={'file': file_stream},
                                    data={filename:
                                        '{"bank": "%s", "account_number": "%s", "currency": "MXN", "rfc_id": %s}' %
                                        (bank, account_number, rfc_id)}).json()

        except WrongDataFormat:
            pass

    def get_bank_transactions(self, sleep_length=30, **kwargs):
        def _request(kwargs):
            return self.make_request(method="GET", path="/banks/bank_transaction", params=kwargs)

        kwargs.setdefault("offset", 0)
        size = kwargs.setdefault("size", 250)

        while True:
            try:
                r = _request(kwargs)
            except TooManyRequests:
                sleep(sleep_length)
                r = _request(kwargs)

            r = r.json()
            if not r['hits']:
                break
            for i in r['hits']:
                yield i
            kwargs["offset"] += size

    def get_bank_transactions_reconciliation(self, rfc_id, reconciliation_id, sleep_length=30, **kwargs):
        try:
            assert (type(reconciliation_id) is int and type(rfc_id) is int), "URL incorrecta"

            def _request(kwargs):
                return self.make_request(method="GET", path="/banks/" + str(rfc_id) + "/transactions/" + str(reconciliation_id) + "/reconciliation/info")

            try:
                r = _request(kwargs)
            except TooManyRequests:
                sleep(sleep_length)
                r = _request(kwargs)

            if r.status_code == 200:
                return r.json()
            else:
                return {"error": r.text, "code": r.status_code}

        except WrongDataFormat:
            pass
