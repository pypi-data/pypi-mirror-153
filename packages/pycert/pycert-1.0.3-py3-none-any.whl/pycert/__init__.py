__author__ = 'Andrey Komissarov'
__date__ = '2021'

import socket
import ssl
import sys
from datetime import datetime
from typing import Union

import plogger
from OpenSSL import crypto
from OpenSSL.crypto import X509
from cryptography import x509
# noinspection PyProtectedMember
from cryptography.hazmat._oid import ObjectIdentifier
from cryptography.hazmat.primitives import hashes
from cryptography.x509 import ExtensionNotFound
from dateutil.parser import parse


class CertClient:
    """Tool to work with server certs"""

    def __init__(self, host: str, port: int = 443, initialize: bool = True, logger_enabled: bool = True):
        """
        :param host:
        :param port:
        :param logger_enabled:
        """

        self.host = host
        self.port = port
        self.logger = plogger.logger('CertClient', enabled=logger_enabled)

        if initialize:
            try:
                self.cert = self.load_certificate()
            except socket.gaierror as err:
                self.logger.exception(f'Invalid host name ({self.host}). Do not use HTTP(S), WWW or "/" in the end.')
                raise ValueError(err)

    # Core methods
    def get_certificate(self) -> str:
        """Retrieve the certificate from the server and return it as a PEM-encoded string"""

        return ssl.get_server_certificate((self.host, self.port))

    def load_certificate(self) -> X509:
        """Load a certificate (X509) from the string or bytes encoded.

        :return: x509
        """

        try:
            log_msg = f'[{self.host}][load_certificate]'
            log_msg += f' -> Load a certificate (X509) from the string or bytes encoded.'
            self.logger.info(log_msg)
            # noinspection PyTypeChecker
            return crypto.load_certificate(crypto.FILETYPE_PEM, buffer=self.get_certificate())
        except crypto.Error as err:
            msg_error = f'Cannot load certificate: {err}'
            self.logger.exception(msg_error)
            raise LookupError(msg_error)

    def _get_all_cert_methods(self) -> list:
        """Service method to get all available parent cert lib methods"""

        x509_cert = self.load_certificate()
        return [i for i in dir(x509_cert) if not i.startswith('_')]

    def get_all_methods(self) -> list:
        """Service method to get all available methods"""

        return [i for i in dir(self) if not i.startswith('_')]

    # -------------- END ---------------------

    # Main methods
    def get_version(self) -> str:
        """Get certificate version. i.e. v3"""
        return self.cert.to_cryptography().version.name

    def get_expiration_date(self) -> datetime:
        """Validity Not After"""

        date_str = self.cert.get_notAfter().decode()
        return parse(date_str, ignoretz=True)

    def get_start_date(self) -> datetime:
        """Validity Not Before"""

        date_str = self.cert.get_notBefore()
        return parse(date_str, ignoretz=True)

    def is_valid(self) -> bool:
        """Auxiliary method to validate "now" is more than valid_from and less than valid_to"""

        self.logger.info(f'[{self.host}][is_valid] Verify certificate validity.')
        now = datetime.now()
        result = self.get_start_date() < now < self.get_expiration_date()
        self.logger.info(f'[{self.host}][is_valid] <- {result}')

        return result

    def get_issuer(self) -> dict:
        """Get issuer info"""

        result = self.cert.get_issuer()
        return {key.decode(): value.decode() for key, value in result.get_components()}

    def get_subject(self) -> dict:
        """Get subject info"""

        result = self.cert.get_subject()
        return {key.decode(): value.decode() for key, value in result.get_components()}

    def is_self_signed(self) -> bool:
        """Compare issuer and subject. It's a self-signed if they are the same"""
        # TODO add authorityKeyIdentifier check to identify self-signing

        return self.get_issuer().get('CN') == self.get_subject().get('CN')

    def get_signature_algorithm(self, brief: bool = True):
        """Get signature hash algorithm.

        :param brief: Returns short name like "sha256". Otherwise returns "sha256WithRSAEncryption"
        :return:
        """

        if brief:
            return self.cert.to_cryptography().signature_hash_algorithm.name
        return self.cert.get_signature_algorithm().decode()

    def get_serial_number(self) -> str:
        """Get serial number in hexadecimal without the first bit"""

        hexadecimal = hex(self.cert.get_serial_number())
        return hexadecimal[2:].upper()

    def get_alt_name(self) -> list:
        """Get Subject Alternative Name.

        oid=2.5.29.17

        Returns list of IPv4Address classes if alt name == IP address
        """

        self.logger.info(f'[{self.host}][get_alt_name] -> Get Subject Alternative Name.')

        extension = self.get_extension_for_oid('2.5.29.17')
        try:
            # noinspection PyTypeChecker
            result = [name.value for name in extension.value]
            self.logger.info(f'[{self.host}][get_alt_name] <- {result}')
            return result
        except AttributeError:
            return []

    # Extensions
    def get_extensions(self) -> Union[x509.extensions.Extensions, None]:
        """Get all available extensions"""
        try:
            return self.load_certificate().to_cryptography().extensions
        except x509.ExtensionNotFound:
            return None

    def get_extension_for_oid(self, oid: str):
        """Get extension by oid.

        https://oidref.com/2.5.4

        :param oid: i.e, "2.5.4.3" for Common name
        :return:
        """

        obj_oid = ObjectIdentifier(oid)
        to_cryptography = self.cert.to_cryptography()

        try:
            return to_cryptography.extensions.get_extension_for_oid(obj_oid)
        except ExtensionNotFound:
            print(f'Extension with oid {oid} not found', file=sys.stderr)

    def get_fingerprint(self, brief: bool = True, algorithm: hashes.HashAlgorithm = None) -> str:
        """Get fingerprint (thumbprint)

        :param brief: 0D4F502EB42A146BD015F8D26837162D4B41415B or 0D:4F:50:2E:B4:2A:14:6B:D0:15:F8...2D4B:41:41:5B
        :param algorithm: instance of SHA1, SHA256, SHA512 etc. classes
        :return:
        """

        self.logger.info(f'[{self.host}][get_fingerprint] -> Get fingerprint (thumbprint). Brief: {brief}')

        algorithm_ = hashes.SHA1() if algorithm is None else algorithm
        fp_raw = self.cert.to_cryptography().fingerprint(algorithm_)
        fp_hex = fp_raw.hex().upper()

        if brief:
            result = fp_hex
        else:
            result = ':'.join(fp_hex[i:i + 2] for i in range(0, len(fp_hex), 2))

        self.logger.info(f'[{self.host}][get_fingerprint] <- {result}')
        return result

    def get_all_info(self, fp_brief: bool = True, signature_algorithm_brief: bool = True) -> dict:
        """Get all consolidated info

        :param fp_brief: 0D4F502EB42A146BD015F8D26837162D4B41415B or 0D:4F:50:2E:B4:2A:14:6B:D0:15:F8...2D4B:41:41:5B
        :param signature_algorithm_brief: sha256 or sha256WithRSAEncryption
        :return:
        """

        self.logger.info(f"[{self.host}][get_all_info] -> Get all certificate's consolidated info")

        try:
            data = {
                'version': self.get_version(),
                'valid_from': self.get_start_date(),
                'valid_to': self.get_expiration_date(),
                'is_valid': self.is_valid(),
                'is_self_signed': self.is_self_signed(),
                'issuer': self.get_issuer(),
                'subject': self.get_subject(),
                'signature_algorithm': self.get_signature_algorithm(brief=signature_algorithm_brief),
                'serial_number': self.get_serial_number(),
                'alternative_name': self.get_alt_name(),
                'fingerprint': self.get_fingerprint(brief=fp_brief),
            }
        except AttributeError as err:
            msg_error = (f'Something went wrong. '
                         f'Perhaps, connection to the server ({self.host}) was not established. '
                         f'Try "initialize=True" parameter. Error: {err}')
            self.logger.exception(msg_error)
            return {}

        self.logger.info(f'[{self.host}][get_all_info] <- {data}')
        return data
