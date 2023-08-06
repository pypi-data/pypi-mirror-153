# -*- coding: utf-8 -*-
from .api import ListoAPI


class Suppliers(ListoAPI):
    def __init__(self, token, base_url):
        super(Suppliers, self).__init__(token, base_url)

    def supplier_list(self, **kwargs):
        """Get all suppliers"""
        # Change param name for endpoint
        if kwargs.get("rfc"):
            kwargs["q"] = kwargs.pop("rfc")

        for s in self.make_request(
                method="GET", path="/counterparties/suppliers/",
                params=kwargs).json()["hits"]:
            yield s

    def import_suppliers(self, rfc, suppliers):
        """Import new Suppliers

        Args:
        - rfc: str of the rfc
        - suppliers: array of dictionaries of suppliers
        """
        return self.make_request(
            method="POST", path="/suppliers/import",
            json={'client_rfc': rfc, 'suppliers': suppliers}
        ).json()
