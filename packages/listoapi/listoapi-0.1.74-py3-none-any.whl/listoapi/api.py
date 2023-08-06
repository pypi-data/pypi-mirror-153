# -*- coding: utf-8 -*-
import re
import requests

from requests import HTTPError

RFC_RE = r"[A-ZÑ&]{3,4}[0-9]{2}[0-1][0-9][0-3][0-9][A-Z,0-9]?[A-Z,0-9]?[0-9,A-Z]?"
DATE_FILTER_RE = r"^([rdmw]:((\d{2,4}-?){3}T(\d{2}:?){3}_?){1,2}|rr:(1_30|31_60|61_90|91\+|today|current_month|previous_month|current_week|previous_week)|all|null)$"


class ListoAPIError(Exception):
    def __init__(self, error_json):
        super(ListoAPIError, self).__init__(error_json)
        self.error_json = error_json


class AuthenticationError(ListoAPIError):
    pass


class PermissionsError(ListoAPIError):
    pass


class ResourceNotFound(ListoAPIError):
    pass


class TooManyRequests(ListoAPIError):
    pass


class ApiError(ListoAPIError):
    pass


class WrongDateFormat(ListoAPIError):
    pass


class WrongRFC(ListoAPIError):
    pass


class WrongDataFormat(ListoAPIError):
    pass

class ListoAPI(object):
    """Listo API Base class

    Args:
        - token (str): Listo API token
    """
    def __init__(self, token, base_url):
        self.token = token
        self.base_url = base_url

    def get_header(self):
        """ Returns authorization header for Listo.mx API """
        return {"Authorization": "Token %s" % self.token}

    def make_request(self, method, path="", url=None, set_header=True, **kwargs):
        """ Base function to handle requests """
        r = requests.request(method, url or (self.base_url + path), headers=self.get_header() if set_header else {}, **kwargs)

        try:
            r.raise_for_status()
            if method == "POST" and r.json()["status"] == "error":
                raise ApiError(r.json())
            return r
        except HTTPError:
            if r.status_code == 401:
                raise AuthenticationError(r.json())
            elif r.status_code == 403:
                raise PermissionsError(r.json())
            elif r.status_code == 404:
                raise ResourceNotFound("Endpoint does not exist %s" % r.url)
            elif r.status_code == 429:
                raise TooManyRequests(r.json())
            else:
                raise ApiError("%s %s" % (r.status_code, r.text))
        except ApiError:
            raise
        # Dev code, maybe delete later
        except KeyError:  # response doesnt include "status" key
            pass
        except ValueError:  # response is not json format
            pass
        except Exception:
            pass

        return r

    """ Others """
    def get_categories(self):
        return self.make_request(method="GET", path="/invoices/categories").json()

    def search_endpoint(self, params):
        return self.make_request(method="GET", path="/invoices/search", params=params)

    @classmethod
    def validate_date_filter(cls, d):
        if not re.match(DATE_FILTER_RE, d):
            raise WrongDateFormat("%s Is not valid filter date, check build_date_filter function" % d)

    @classmethod
    def validate_rfc(cls, rfc):
        if not re.match(RFC_RE, rfc):
            raise WrongRFC("%s Does not match RFC structure" % rfc)
