# -*- coding: utf-8 -*-
import base64
import ssl
import requests
import sys
import os
import subprocess

from OpenSSL import crypto
from .api import ListoAPI, ResourceNotFound


class InvalidRFCId (ResourceNotFound):
    pass

class InvoicingMixin(ListoAPI):
    # Private for create XML
    def _generate_xml(self, generation_data):
        return self.make_request(method="POST", json=generation_data,
                                 path="/invoicing/generate_xml")

    # Private send data and XML to certify in Listo.mx
    def _certify_xml(self, certification_data):
        return self.make_request(method="POST", json=certification_data,
                                 path="/invoicing/certify_xml")

    # Private send cancel request
    def _cancel(self, certification_data, path):
        return self.make_request(method="POST", json=certification_data,
                                 path=path)

    # Private replace certificate number in original chain
    def _format_original_chain(self, g_xml):
        return g_xml['original_chain'].replace('|' + '0' * 20 + '|', '|%s|' % self.certificate_num)

    def email_invoice(self, gid, **kwargs):
        """Email invoice
        Args:
            gid: invoice.generated_invoice_id, do not mistake with invoice.id. In that case use Invoices.send_by_email
            from: email who will send it
            to: receiver email
            subject: email subject
            text: Message body in text
            html: Message body in html format
        """
        return self.make_request(method="POST", json=kwargs,
                                 path="/invoicing/invoices/%s/email" % gid)

    def get_customer_rfcs(self):
        """Data from default_rfc_id, employees, receivers, issuers and branches """
        return self.make_request(method="GET", path="/invoicing/customer/rfcs/").json()

class InvoicingVault(InvoicingMixin):
    """InvoicingVault class
    Args:
        - token (str): Listo API token
        - certificate_num(str): Numero del certificado que se va a usar
        - cer_path(str): Opcional. Path del certificado .cer
    """
    def __init__(self, token, base_url, certificate_num, cer_path=None):
        super(InvoicingVault, self).__init__(token, base_url)
        self.certificate_num = certificate_num
        self.cer_path = cer_path

    # Private get the vault private key id, certificate number and rfc id
    def _get_signature_data(self, request_rfc):
        issuer_vault = [(issuer['vault_private_keys'], issuer['id']) for issuer in self.get_customer_rfcs()['issuers'] if issuer['rfc'] == request_rfc]
        if not issuer_vault:
            raise InvalidRFCId("rfc {} is not registered".format(request_rfc))

        cert_list = issuer_vault[0][0]
        self.rfc_id = issuer_vault[0][1]

        key_id_list = [cert['id'] for cert in cert_list if cert['certificate_num'] == self.certificate_num]
        if not key_id_list:
            raise InvalidRFCId("rfc {} does not have a private key saved in the vault".format(request_rfc))

        self.key_id = key_id_list[0]

    # Private download the public certificate and load it
    def _get_certificate(self):
        if not self.cer_path:
            url = "https://rdc.sat.gob.mx/rccf/{0}/{1}/{2}/{3}/{4}/{5}.cer".format(
                self.certificate_num[0:6], self.certificate_num[6:12], self.certificate_num[12:14],
                self.certificate_num[14:16], self.certificate_num[16:18], self.certificate_num
            )
            csd = requests.get(url, timeout=10, verify=False)
            self.cert_der = csd.content
        else:
            with open(self.cer_path, 'rb') as f:
                self.cert_der = f.read()
        self.cert = crypto.load_certificate(crypto.FILETYPE_PEM, ssl.DER_cert_to_PEM_cert(self.cert_der))

    def generate(self, generation_data, rfc, certify=False, permanent_urls=False):
        """Generate XML, Sign it and get SAT stamp

        Args:
            - generation_data ([]): array of invoice data to generate
            - certify (bool): If True do not send to SAT for stamping. Default True
        """
        # Validate data
        for g_data in generation_data:
            self.validate_rfc(g_data["issuer"]["rfc"])
            self.validate_rfc(g_data["receiver"]["rfc"])

        # Get rfc_id, key_id and certificate_num
        try:
            self._get_signature_data(rfc)
        except ResourceNotFound:
            raise InvalidRFCId("rfc {} does not have a private key saved in the vault".format(rfc))

        # Get certificate
        self._get_certificate()

        # Generate XML
        try:
            generated_xml = self._generate_xml(generation_data).json()
        except ResourceNotFound:
            raise InvalidRFCId("issuer.id %s does not match token's user" % generation_data["issuer"]["id"])

        for g_xml, g_data in zip(generated_xml, generation_data):
            # g_xml contains xml and original_chain
            xml = g_xml['xml']

            original_chain = self._format_original_chain(g_xml)

            # Verification and signature
            data = {
                'rfc_id': self.rfc_id,
                'key_id': self.key_id,
                'message': original_chain
            }
            signature = self.make_request(method="POST", json=data,
                                          path="/invoicing/sign_using_private_key").json()
            decoded_signature = base64.b64decode(signature['signature'])
            crypto.verify(self.cert, decoded_signature, original_chain, 'sha256')

            # Object to stamp
            certification_data = {
                'xml': xml,
                'certificate_num': self.certificate_num,
                'certificate': base64.b64encode(self.cert_der).decode("utf-8"),
                'signature': base64.b64encode(decoded_signature).decode("utf-8"),
                'data': g_data,
                'permanent_urls': permanent_urls
            }
            if certify:
                r = self._certify_xml(certification_data).json()
                yield r, certification_data, original_chain
            else:
                yield {}, certification_data, original_chain

    def cancel(self, invoice_id, rfc, cfdi_kind="invoice", reason=None, substituted_by_uuid=None):
        """Cancel Invoice
        Args:
            invoice_id (str or int): invoice.id
            cfdi_kind (str): Kind of CFDI to cancel. invoice or withholding (Optional)
            rfc (str): Issuer RFC
            reason (str: optional):
                “01” Comprobantes emitidos con errores con relación.
                “02” Comprobantes emitidos con errores sin relación.
                “03” No se llevó a cabo la operación.
                “04” Operación nominativa relacionada en una factura global.
            substituted_by_uuid (str: optional-conditional): New invoice's UUID which replace the current CFDI
        """
        # Validate data
        self.validate_rfc(rfc)

        # Get rfc_id, key_id and certificate_num
        try:
            self._get_signature_data(rfc)
        except ResourceNotFound:
            raise InvalidRFCId("rfc {} does not have a private key saved in the vault".format(rfc))

        # Get certificate
        self._get_certificate()

        data = {
            'rfc_id': self.rfc_id,
            'key_id': self.key_id,
            'message': base64.b64encode(self.cert_der).decode("utf-8"),
            "reason": reason,
            "substituted_by_uuid": substituted_by_uuid
        }
        return self.make_request(method="POST", json=data, path=f"/invoicing/cancel_using_vault_private_key/{cfdi_kind}/{invoice_id}/").json()

class Invoicing(InvoicingMixin):
    """Invoicing class
    Args:
        - token (str): Listo API token
        - cer_path (str): Path to the .cer file
        - key_path (str): Path to the .key file
        - key_passphrase (str): .key file password
    """
    def __init__(self, token, cer_path, key_path, key_passphrase, base_url):
        super(Invoicing, self).__init__(token, base_url)
        self.CER_PATH = cer_path
        self.KEY_PATH = key_path
        self.PRIVATE_KEY_PASSPHRASE = key_passphrase

        self._read_cer()
        self._read_key()

    # Private for read certificate
    def _read_cer(self):
        with open(self.CER_PATH, 'rb') as f:
            self.cert_der = f.read()
            self.cert = crypto.load_certificate(
                crypto.FILETYPE_PEM, ssl.DER_cert_to_PEM_cert(self.cert_der))
        self.certificate_num = ('%0x' % self.cert.get_serial_number())[1::2]

    # Private for read key
    def _read_key(self):
        with open(self.KEY_PATH, 'rb') as f:
            self.private_key_der = f.read()

        if 'win' in sys.platform:
            args = ['%s/openssl' % os.path.dirname(os.path.realpath(__file__)), 'pkcs8', '-inform', 'DER', '-passin', 'pass:' + self.PRIVATE_KEY_PASSPHRASE]
        else:
            args = ['openssl', 'pkcs8', '-inform', 'DER', '-passin', 'pass:' + self.PRIVATE_KEY_PASSPHRASE]
        proc = subprocess.Popen(
            args, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        private_pem = proc.communicate(input=self.private_key_der)[0].strip()
        self.key = crypto.load_privatekey(crypto.FILETYPE_PEM, private_pem)

    def cancel(self, gid, reason=None, substituted_by_uuid=None):
        """Cancel Invoice
        Args:
            gid: invoice.generated_invoice_id, do not mistake with invoice.id
            reason (str: optional):
                “01” Comprobantes emitidos con errores con relación.
                “02” Comprobantes emitidos con errores sin relación.
                “03” No se llevó a cabo la operación.
                “04” Operación nominativa relacionada en una factura global.
            substituted_by_uuid (str: optional-conditional): New invoice's UUID which replace the current CFDI
        """
        cd = {
            "certificate_der": base64.b64encode(self.cert_der).decode("utf-8"),
            "passcode": self.PRIVATE_KEY_PASSPHRASE,
            "private_key_der": base64.b64encode(self.private_key_der).decode("utf-8"),
            "reason": reason,
            "substituted_by_uuid": substituted_by_uuid
        }
        return self._cancel(cd, "/invoicing/cancel/invoice/{}/".format(gid)).json()

    def generate(self, generation_data, certify=False, permanent_urls=False):
        """Generate XML, Sign it and get SAT stamp

        Args:
            - generation_data ([]): array of invoice data to generate
            - testing (bool): If True do not send to SAT for stamping. Default True
        """
        # Validate data
        for g_data in generation_data:
            self.validate_rfc(g_data["issuer"]["rfc"])
            self.validate_rfc(g_data["receiver"]["rfc"])

        # Generate XML
        try:
            generated_xml = self._generate_xml(generation_data).json()
        except ResourceNotFound:
            raise InvalidRFCId("issuer.id %s does not match token's user" % generation_data["issuer"]["id"])

        for g_xml, g_data in zip(generated_xml, generation_data):
            # g_xml contains xml and original_chain
            xml = g_xml['xml']

            original_chain = self._format_original_chain(g_xml)

            # Verification and signature
            signature = crypto.sign(self.key, original_chain, 'sha256')
            crypto.verify(self.cert, signature, original_chain, 'sha256')

            # Object to stamp
            certification_data = {
                'xml': xml,
                'certificate_num': self.certificate_num,
                'certificate': base64.b64encode(self.cert_der).decode("utf-8"),
                'signature': base64.b64encode(signature).decode("utf-8"),
                'data': g_data,
                'permanent_urls': permanent_urls
            }

            if certify:
                r = self._certify_xml(certification_data).json()
                yield r, certification_data, original_chain
            else:
                yield {}, certification_data, original_chain
