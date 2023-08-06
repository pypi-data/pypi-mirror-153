# -*- coding: utf-8 -*-
from .api import ListoAPI


class Purchases(ListoAPI):
    def __init__(self, token, base_url):
        super(Purchases, self).__init__(token, base_url)

    def goods_receipts_nums(self, **kwargs):
        return self.make_request(
            method="GET", path="/purchases/goods_receipts/nums/",
            params=kwargs).json()

    def purchase_orders(self, **kwargs):
        """Get purchase orders"""
        kwargs.setdefault("offset", 0)
        size = kwargs.setdefault("size", 250)
        while True:
            r = self.make_request(
                method="GET", path="/purchases/purchase_orders/",
                params=kwargs).json()["hits"]
            if not r:
                break
            for i in r:
                yield i
            kwargs["offset"] += size

    def import_purchase_orders(self, rfc, items):
        """Import new Purchase orders

        Args:
        - rfc: str of the rfc
        - items: array of dictionaries of purchase orders
        """
        return self.make_request(
            method="POST", path="/purchases/purchase_orders/import",
            json={'client_rfc': rfc, 'items': items}
        ).json()

    def goods_receipts(self, **kwargs):
        """Get goods receipts"""
        kwargs.setdefault("offset", 0)
        size = kwargs.setdefault("size", 250)
        while True:
            r = self.make_request(
                method="GET", path="/purchases/goods_receipts/",
                params=kwargs).json()["hits"]
            if not r:
                break
            for i in r:
                yield i
            kwargs["offset"] += size

    def import_goods_receipts(self, rfc, items):
        """Import new Goods receipts

        Args:
        - rfc: str of the rfc
        - items: array of dictionaries of goods receipts
        """
        return self.make_request(
            method="POST", path="/purchases/goods_receipts/import",
            json={'client_rfc': rfc, 'items': items}
        ).json()
