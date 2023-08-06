import logging
import requests
import json
import urllib

from odoo_somconnexio_python_client import helpers
from odoo_somconnexio_python_client import exceptions


logger = logging.getLogger(__name__)


class Client(object):
    """Client class
    This class manage the HTTP requests and only this class can send a request.

    We need to be able the environmnet variables needed to connect with the Odoo instance:
    * ODOO_BASEURL
    * ODOO_APIKEY
    """

    def __init__(self):
        self.baseurl = helpers.getenv_or_fail("ODOO_BASEURL")
        self.api_key = helpers.getenv_or_fail("ODOO_APIKEY")

    def get(self, route, params={}, extra_headers={}):
        """Send a GET HTTP requests

        Args:
            route (str): String with the route to the endpoint

        Return:
            **response**: Return the response object
        """
        return self._send_request(
            verb="GET",
            url=self._format_url(route),
            params=params,
            extra_headers=extra_headers,
        )

    def post(self, route, body):
        """Send a POST HTTP requests

        Args:
            route (str): String with the route to the endpoint
            body (dict): Dict with the body of the request to send

        Return:
            **response**: Return the response object
        """
        headers = {
            "Content-Type": "application/json",
        }
        return self._send_request(
            verb="POST",
            url=self._format_url(route),
            payload=body,
            extra_headers=headers,
        )

    def _format_url(self, path):
        path = "/api" + path
        return urllib.parse.urljoin(self.baseurl, path)

    def _send_request(self, verb, url, payload=None, params={}, extra_headers={}):
        """send the API request using the *requests.request* method

        Args:
            payload (dict)

        Raises:
            OTRSHTTPError:
            ArgumentMissingError

        Returns:
            **requests.Response**: Response received after sending the request.

        .. note::
            Supported HTTP Methods: DELETE, GET, HEAD, PATCH, POST, PUT
        """
        headers = {
            "Accept": "application/json",
            "API-KEY": self.api_key,
        }
        if extra_headers:
            headers.update(extra_headers)

        json_payload = None
        if payload:
            json_payload = json.dumps(payload)
            logger.info(
                "{verb} {url} \n {body}".format(verb=verb, url=url, body=payload)
            )
        else:
            logger.info(
                "{verb} {url} \n {body}".format(verb=verb, url=url, body=params)
            )

        try:
            response = requests.request(
                verb.upper(), url, headers=headers, data=json_payload, params=params
            )
        except Exception as err:
            raise exceptions.HTTPError(err)
        if response.status_code == 500:
            raise exceptions.HTTPError(response.reason)
        if response.status_code != 200:
            return None
        return response.json()
