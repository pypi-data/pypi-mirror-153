# -*- coding: utf-8 -*-
from time import sleep
from .api import ListoAPI, TooManyRequests
from datetime import datetime


class Invoices(ListoAPI):
    def __init__(self, token, base_url):
        super(Invoices, self).__init__(token, base_url)

    def _validate_date_filters(self, kwargs):
        for d in ["issued_on", "due_on", "modified_on", "canceled_on", "paid_on"]:
            if kwargs.get(d):
                self.validate_date_filter(kwargs.get(d))

    def set_category(self, invoice_id, category_id):
        """Modify an Invoice category

        Args:
            - invoice_id (str|int): id of the invoice
            - category_id (str|int): id of the category

        Check available categories with get_categories()
        """
        return self.make_request(method="POST", path="/invoices/update_category/%s" % invoice_id,
                                 json={'category_id': category_id}).json()

    def add_payment(self, invoice_id, bank_account, amount, amount_mxn, effective_on,
                    reimbursed_on=None, reimbursable_to=None, description=None, group_id=None, data=None):
        """Register a payment to an Invoice

        Args:
            - invoice_id (str|int): id of the invoice
            - bank_account (str|int): last 4 numbers of the bank account
            - amount (str|int): amount of the payment
            - effective_on (datetime|str): datetime or ISO 8601 format (YYYY-MM-DDTHH:mm:ss)
            - reimbursed_on (datetime|str): datetime or ISO 8601 format (YYYY-MM-DDTHH:mm:ss)
            - reimbursable_to (str): Description of the reimbursement
            - description (str): Description of the paymnet
            - group_id (str|int): Unique identifier to group many invoices by payment
            - data (json): Json to store extra_data

        Check available categories with get_categories()
        """
        return self.make_request(method="POST", path="/invoices/%s/payments/" % invoice_id,
                                 json=dict(bank_account=bank_account, amount=amount, amount_mxn=amount_mxn,
                                           effective_on=effective_on, reimbursed_on=reimbursed_on,
                                           reimbursable_to=reimbursable_to, description=description, group_id=group_id, data=data)).json()

    def delete_payments(self, invoice_id):
        """Delete all payments from an invoice

        Args:
            - invoice_id (str|int): id of the invoice
        """
        return self.make_request(method="POST", path="/invoices/mark_as_unpaid/%s" % invoice_id).json()

    def delete_payment_with_id(self, invoice_id, payment_id):
        """Delete specific payment from an invoice

        Args:
            - invoice_id (str|int): id of the invoice
            - payment_id (str|int): id of the payment
        """
        return self.make_request(method="DELETE", path=f"/invoices/{invoice_id}/payments/{payment_id}/")

    def set_dimension(self, invoice_id, dimension_name, dimension_value):
        """Set a dimension value

        Args:
            - invoice_id (str|int): id of the invoice
            - dimension_name (str): name of the dimension
            - invoice_id (str): new value of the dimension
        """
        return self.make_request(method="POST", path="/invoices/set_dimension/%s" % invoice_id,
                                 json=dict(name=dimension_name, value=dimension_value)).json()

    def count_search(self, **kwargs):
        """Get search count

        kwargs: Same as search()
        """
        # Change param name for endpoint
        if kwargs.get("uuid") or kwargs.get("amount"):
            kwargs["q"] = kwargs.pop("uuid") if kwargs.get("uuid") else kwargs.pop("amount")

        kwargs['limit'] = 1
        return self.make_request(method="GET", path="/invoices/export_json",
                                 params=kwargs).json()['count']

    def search(self, sleep_length=30, method="GET", export_json=True, **kwargs):
        """Search invoices by some fields

        kwargs:
            - uuid (str): uuid of the invoice
            - uuids ([str]): list of invoice uuids
            - ids ([int]): array of invoice ids
            - is_payroll (bool)
            - amount (int|float): If given an integer amount, search for rounded amount (e.g. $861 could be ~ 860.50 to 861.50). Otherwise search for an exact match +- 1 cent
            - rfc_id (int|str): Id of the rfc in Listo
            - counterparty (str): RFC of the counterparty
            - series (str): Series of the invoice
            - folio (int|str): Folio of the invoice
            - category_id (str|[str]): income, expenses, null, id de category_id
            - payment_state (str|[str]): reimbursable, pending_approved, paid
            - adjusted_subtotal_mxn (int|float):
            - total_mxn
            - exclude_canceled
            - accounting_export_state
            - issued_on (str): ISO 8601 datetime (YYYY-MM-DDTHH:mm:ss)
            - due_on (str): ISO 8601 datetime (YYYY-MM-DDTHH:mm:ss)
            - modified_on (str): ISO 8601 datetime (YYYY-MM-DDTHH:mm:ss)
            - canceled_on (str): ISO 8601 datetime (YYYY-MM-DDTHH:mm:ss)
            - paid_on (str): ISO 8601 datetime (YYYY-MM-DDTHH:mm:ss)
            - size (default=250)
            - offset (default=0)
        """
        if export_json:
            subdirectory = 'export_json'
            results_type = 'results'
        else:
            subdirectory = 'search'
            results_type = 'hits'

        def _request(kwargs):
            print(kwargs)
            # Chosse between params or json depending on method
            if method == 'GET':
                return self.make_request(
                    method=method, path='/invoices/%s' % subdirectory,
                    params=kwargs)
            else:
                return self.make_request(
                    method=method, path='/invoices/%s' % subdirectory,
                    data=kwargs, params={'offset': kwargs['offset'], 'size': kwargs['size']})

        # Validate date filters
        self._validate_date_filters(kwargs)

        # Change param name for endpoint
        if kwargs.get("uuid") or kwargs.get("amount"):
            kwargs["q"] = kwargs.pop("uuid") if kwargs.get("uuid") else kwargs.pop("amount")

        kwargs.setdefault("offset", 0)
        size = kwargs.setdefault("size", 250)
        while True:
            try:
                r = _request(kwargs)
            except TooManyRequests:
                sleep(sleep_length)
                r = _request(kwargs)

            r = r.json()
            if not r[results_type]:
                break
            for i in r[results_type]:
                yield i
            kwargs["offset"] += size

    def workflow(self, name, status, method="GET", sleep_length=30, **kwargs):
        """Search invoices in a workflow

        kwargs:
            - ids ([int]): list of invoice ids
            - since (str): ISO 8601 datetime (YYYY-MM-DDTHH:mm:ss)
            - created_since (str): ISO 8601 datetime (YYYY-MM-DDTHH:mm:ss)
            - fields ([str]): list of fields to display (optional)
            - issued_on (str): ISO 8601 datetime (YYYY-MM-DDTHH:mm:ss)
            - has_pdf (str): false | true
            - bank (str): last 4 numbers | credit
            - counterparty (str): RFC of the counterparty
            - folio (int|str): Folio of the invoice
            - total_mxn (float|str):
            - rfc_id (int|str): Id of the rfc in Listo
            - extra_data (str): JSON
            - on_hold (str): true|false
            - size (default=250)
            - offset (default=0)
        """
        def _request(kwargs):
            # Chosse between params or json depending on method
            if method == 'GET':
                return self.make_request(
                    method=method, path="/workflow/%s/%s" % (name, status),
                    params=kwargs)
            else:
                return self.make_request(
                    method=method, path="/workflow/%s/%s" % (name, status),
                    json=kwargs, params={'offset': kwargs['offset'], 'size': kwargs['size']})

        # Validate date filters
        self._validate_date_filters(kwargs)

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
            for i in r:
                yield i
            kwargs["offset"] += size

    def details(self, invoice_id):
        """Invoice details

        Args:
            - invoice_id (int|str): Invoice id

        More information at https://apidocs.listo.mx/#detalle-de-factura
        """
        return self.make_request(method="GET", path="/invoices/%s" % invoice_id).json()

    def send_by_email(self, iid, **kwargs):
        """Email invoice
        Args:
            iid: invoice id
            from: email who will send it
            to: receiver email
            subject: email subject
            attachments: Ids of the documents to attach
        """
        return self.make_request(method="POST", json=kwargs,
                                 path="/invoices/%s/send_by_email" % iid).json()

    def mark_as_approved(self, iid, **kwargs):
        """Mark approved invoice
        Args:
            - iid: invoice_id (int|str): Invoice id
            - approved_rejected_on: (str): ISO 8601 datetime (YYYY-MM-DDTHH:mm:ss)
        """
        try:
            datetime.strptime(kwargs['approved_rejected_on'], '%Y-%m-%dT%H:%M:%S')
        except Exception as e:
            return e

        return self.make_request(method="POST", json=kwargs,
                                 path="/invoices/mark_as_approved/{}".format(iid)).json()

    def update_due_on(self, iid, **kwargs):
        """Update due_on for invoice
        Args:
            - iid: invoice_id (int|str): Invoice id
            - due_on: (str): ISO 8601 datetime (YYYY-MM-DDTHH:mm:ss)
        """
        try:
            datetime.strptime(kwargs['due_on'], '%Y-%m-%dT%H:%M:%S')
        except Exception as e:
            return e

        return self.make_request(method="POST", json=kwargs,
                                 path="/invoices/update_due_on/{}".format(iid)).json()
