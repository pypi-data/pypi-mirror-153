# -*- coding: utf-8 -*-
from .api import ListoAPI


class Setup(ListoAPI):
    def __init__(self, token, base_url):
        super(Setup, self).__init__(token, base_url)

    def validate_ciec(self, rfc, ciec):
        """Validate ciec password for a RFC

        Args:
            - rfc (str): RFC of the business
            - ciec (str): CIEC password
        """
        return self.make_request(method="POST", path="/signup/verify_ciec", json=dict(rfc=rfc, ciec=ciec)).json()

    def add_main_user(self, rfc, ciec, sat_sync_since="2016-01-01", sat_sync_webhook_url=""):
        """Register a new business

        Args:
            - rfc (str): RFC of the business
            - ciec (str): CIEC password
            - sat_sync_since (str): ISO format YYYY-mm-dd date from which invoices will download
            - sat_sync_webhook_url (str): Webhook URL to receive notifications after successful downloads
        """
        return self.make_request(method="POST", path="/signup/external", json=dict(rfc=rfc, ciec=ciec,
                                 sat_sync_since=sat_sync_since, sat_sync_webhook_url=sat_sync_webhook_url)).json()

    def modify_ciec(self, rfc_id, ciec):
        """Change CIEC password for an rfc_id

        Args:
            - rfc_id (str|int)
            - ciec (str): new ciec password
        """
        return self.make_request(method="POST", path="/customers/rfcs/%s/enable_sat_sync" % rfc_id,
                                 json={"ciec": ciec}).json()

    def view_rfcs(self):
        """List all rfcs the token has access to"""
        return self.make_request(method="GET", path="/customers/rfcs/").json()

    def lookup_rfc(self, rfc):
        """List all rfcs the token has access to"""
        return self.make_request(method="GET", path="/signup/lookup_rfc/%s" % rfc).json()

    def add_rfc(self, **kwargs):
        """Add rfc to a user

        Kwargs:
        - colonia
        - ext_num
        - int_num
        - locality
        - mailbox_suffix: <main_username>+<mailbox_suffix>@buzon.listo.mx
        - municipio
        - postal_code
        - rfc
        - rfc_name
        - state
        - street
        - tax_regime: Possible values are {pf_asalariado, pf_profesional, pf_rif, pm, pm_nonprofit}
        """
        return self.make_request(method="POST", path="/customers/rfcs/", data=kwargs).json()

    def disable_sat_sync(self, rfc_id):
        """
        Args:
            - rfc_id (str|int)
        """
        return self.make_request(method="POST", path="/customers/rfcs/%s/disable_sat_sync" % rfc_id).json()

    def prefsAPI(self, **kwargs):
        """  Configuración de preferencia de descarga
            true:  para habilitar la descarga de ese tipo de CFDI
            false: para NO descargar ese tipo de CFDI
            only : para únicamente descargar ese tipo CFDI

            Parameters:
                sat_sync_issued (bool|str): para descargar CFDIs emitidos
                sat_sync_payroll  (bool|str): para descargar CFDIs de nómina
                sat_sync_received (bool|str): para descargar CFDIs recividos
                sat_sync_crp (bool|str): para descargar CFDIs de complementos de pago
                sat_sync_since (str): Fecha de inicio de descarga de histórico de facturas. (Formato ISO YYYY-mm-dd)
                sat_sync_until (str): Fecha hasta la cual se deben descargar los CFDIs . (Formato ISO YYYY-mm-dd)
            Returns:
                json: {"status": "ok"}
            Example:
                ```python
                from listoapi import ListoApi
                api = ListoApi("<api_key>")
                api.Setup.prefsAPI(sat_sync_issued=only)
                # returns: {"status": "ok"}
                ```
        """
        return self.make_request(method="POST", path="/customers/prefs", data=kwargs).json()

    def pause_sat_sync(self, rfc_id):
        """  Pausar descarga automática
            Parameters:
                rfc_id (str|int)
            Returns:
                json: {"status": "ok"}
            Example:
                ```python
                from listoapi import ListoApi
                api = ListoApi("<api_key>")
                api.Setup.pause_sat_sync(rfc_id=3)
                # returns: {"status": "ok"}
                ```
        """
        return self.make_request(method="POST", path="/customers/rfcs/%s/pause_sat_sync" % rfc_id).json()

    def resume_sat_sync(self, rfc_id):
        """  Reanudar descarga automática
            Parameters:
                rfc_id (str|int)
            Returns:
                json: {"status": "ok"}
            Example:
                ```python
                from listoapi import ListoApi
                api = ListoApi("<api_key>")
                api.Setup.pause_sat_sync(rfc_id=3)
                # returns: {"status": "ok"}
                ```
        """
        return self.make_request(method="POST", path="/customers/rfcs/%s/resume_sat_sync" % rfc_id).json()
