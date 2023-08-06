from .documents import Documents as _documents
from .invoices import Invoices as _invoices
from .invoicing import Invoicing as _invoicing
from .invoicing import InvoicingVault as _invoicing_vault
from .items import Items as _items
from .setup import Setup as _setup
from .cfdi_payments import CfdiPayments as _cfdi_payments
from .expenses import Expenses as _expenses
from .banks import Banks as _banks
from .purchases import Purchases as _purchases
from .suppliers import Suppliers as _suppliers
from .exchange_rate import ExchangeRate as _er
from .cash_advances import CashAdvances as _cash_advances
from .reports import Reports as _reports
from .filings import Filings as _filings
from .payments import Payments as _payments
from .api import AuthenticationError, PermissionsError, ResourceNotFound, TooManyRequests, ApiError
from datetime import datetime


class ListoApi():
    def __init__(self, token, cer_path=None, key_path=None, key_passphrase=None, certificate_num=None, is_vault=False, base_url="https://listo.mx/api"):
        self.Documents = _documents(token, base_url)
        self.Invoices = _invoices(token, base_url)
        self.Items = _items(token, base_url)
        self.Setup = _setup(token, base_url)
        self.CfdiPayments = _cfdi_payments(token, base_url)
        self.Expenses = _expenses(token, base_url)
        self.Banks = _banks(token, base_url)
        self.Purchases = _purchases(token, base_url)
        self.Suppliers = _suppliers(token, base_url)
        self.ExchangeRate = _er(token, base_url)
        self.CashAdvances = _cash_advances(token, base_url)
        self.Filings = _filings(token, base_url)
        self.Reports = _reports(token, base_url)
        self.Payments = _payments(token, base_url)
        if is_vault:
            self.InvoicingVault = _invoicing_vault(token, base_url, certificate_num, cer_path)
        if cer_path and key_path and key_passphrase:
            self.Invoicing = _invoicing(token, cer_path, key_path, key_passphrase, base_url)

    @staticmethod
    def build_date_filter(last_n_days=None, start=None, end=None, specific="month"):
        """Return date string for listo API endpoints

        Args:
            - start (date)
            - end (date)
            - last_n_days (int)
            - specific (str) "day", "week" or "month". Default month

        Returns:
            - d:YYYY-mm-ddT00:00:00 Specific day
            - w:YYYY-mm-ddT00:00:00 Specific week
            - m:YYYY-mm-ddT00:00:00 Specific month
            - r:YYYY-mm-ddT00:00:00_YYYY-mm-ddT00:00:00 Date range
            - rr:last60d Last 60 days
            - rr:last30d Last 30 days
            - rr:last14d Last 14 days
            - rr:last7d Last 7 days
        """
        if type(start) is datetime:
            start = start.date()
        if type(end) is datetime:
            end = end.date()

        if last_n_days:
            assert last_n_days in [60, 30, 14, 7], "last_n_days must be 60, 30 14 or 7"
            return "rr:last%sd" % last_n_days
        elif end:
            return "r:%sT00:00:00_%sT00:00:00" % (start.isoformat(), end.isoformat())
        elif specific == "day":
            return "d:%sT00:00:00" % start.isoformat()
        elif specific == "week":
            return "w:%sT00:00:00" % start.isoformat()
        else:
            return "m:%sT00:00:00" % start.isoformat()
