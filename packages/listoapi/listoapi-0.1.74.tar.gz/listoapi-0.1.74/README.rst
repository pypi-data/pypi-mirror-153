Listo SDK module for web API integration
===============================================

* `Install`_
* `Documentation`_

Install
-------

``pip install listoapi``

Documentation
--------------

Complete documentation can be found at `https://apidocs.listo.mx/ <https://apidocs.listo.mx/>`_.

Start
~~~~~~~~~~~~~~~~~~~~~~

::

    from listoapi import ListoApi

    api = ListoApi("your_listo_token")

Search invoices
~~~~~~~~~~~~~~~~~~~~~~

::

    invoice = next(api.Invoices.search(uuid="00112233-4455-6677-8899-AABBCCDDEEFF"))

or

::

    for invoice in api.Invoices.search(issued_on="m:2018-05-01T00:00:00"):
        # Your code

Full details of invoice
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    api.Invoices.details(invoice['id'])

Add or delete payments
~~~~~~~~~~~~~~~~~~~~~~

::

    api.Invoices.add_payment(invoice['id'], bank_account=1234, amount=200, amount_mxn=200,
                             effective_on=""2018-07-24T00:00:00)
    api.Invoices.delete_payments(invoice['id'])

Generate invoice
~~~~~~~~~~~~~~~~~~~~~~

::

    api = ListoApi("your_listo_token", "path/to/cer/file.cer", "path/to/key/file.key", "key_password")
    generation_data = [{...}]

    res, certification_data, original_chain = next(api.Invoicing.generate(generation_data, staging=False, certify=True))
