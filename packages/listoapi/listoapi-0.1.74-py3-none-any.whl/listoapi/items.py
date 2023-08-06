# -*- coding: utf-8 -*-
from time import sleep
from .api import ListoAPI, TooManyRequests


class Items(ListoAPI):
    def __init__(self, token, base_url):
        super(Items, self).__init__(token, base_url)

    def _validate_date_filters(self, kwargs):
        for d in ["issued_on", "due_on", "modified_on", "canceled_on", "paid_on"]:
            if kwargs.get(d):
                self.validate_date_filter(kwargs.get(d))

    def get(self, item_type, sleep_length=30, **kwargs):
        """Search items by fields

        kwargs:
            It will depend on the item configuration fields at 'listo console -> items -> fields'

        """

        # Validate date filters
        self._validate_date_filters(kwargs)

        kwargs.setdefault("offset", 0)
        size = kwargs.setdefault("size", 100)
        while True:
            try:
                r = self.make_request(
                    method="GET", path="/items/%s/" % item_type,
                    params=kwargs)
            except TooManyRequests:
                sleep(sleep_length)
                r = self.make_request(
                    method="GET", path="/items/%s/" % item_type,
                    params=kwargs)

            r = r.json()
            if not r['hits']:
                break
            for i in r['hits']:
                yield i
            kwargs["offset"] += size

    def import_items(self, item_type, items):
        """Add items

        items must be an array of dicts. With fields depending on item_type
        """
        return self.make_request(
            method="POST", path="/items/%s/import_items/" % item_type,
            json=items).json()

    def update_field(self, item_type, iid, name, value):
        """Update field of item

        kwargs:
        - item_type: name of Item
        - id: id of item to modify
        - name: name of field
        - value: new value
        """
        return self.make_request(
            method="POST", path="/items/%s/%s/update_field/" % (item_type, iid),
            json=dict(name=name, value=value)).json()

    def batch_update_items(self, item_type, new_data):
        """Update field of item

        kwargs:
        - item_type: name of Item
        - new_data: list with dictionaries of items.
            Items must contain 'num' key and any field that will be updated
        """
        return self.make_request(
            method="POST", path="/items/%s/batch_update_items/" % item_type,
            json=new_data).json()

    def reset_items(self, item_type, num=None):
        """WARNING! This deletes all items

        kwargs:
        - item_type: name of Item
        - new_data: list with dictionaries of items.
            Items must contain 'num' key and any field that will be updated
        """
        return self.make_request(
            method="POST", path="/items/%s/reset_items/" % item_type,
            json={'num': num}).json()
