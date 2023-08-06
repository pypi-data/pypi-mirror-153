from __future__ import unicode_literals  # support both Python2 and 3

from mock import patch

import unittest2 as unittest

from ..settings import REQUIRED_ENVVARS
from odoo_somconnexio_python_client.resources.provider import Provider


@patch("odoo_somconnexio_python_client.resources.provider.Client.get")
@patch.dict("os.environ", REQUIRED_ENVVARS)
class ProviderTests(unittest.TestCase):
    def test_get_mobile_list(self, client_get_mock):

        provider_names = ["provider1", "provider2", "provider3"]
        expected_response = {
            "count": 3,
            "providers": [
                {"id": 1, "name": provider_names[0]},
                {"id": 2, "name": provider_names[1]},
                {"id": 3, "name": provider_names[2]},
            ],
        }

        client_get_mock.return_value = expected_response

        providers = Provider.mobile_list()

        client_get_mock.assert_called_with(
            "/provider", params={"mobile": "true", "broadband": "false"}
        )

        for p in providers:
            self.assertIn(p.name, provider_names)

    def test_get_broadband_list(self, client_get_mock):

        provider_names = ["provider1", "provider2", "provider3"]
        expected_response = {
            "count": 3,
            "providers": [
                {"id": 1, "name": provider_names[0]},
                {"id": 2, "name": provider_names[1]},
                {"id": 3, "name": provider_names[2]},
            ],
        }

        client_get_mock.return_value = expected_response

        providers = Provider.broadband_list()

        client_get_mock.assert_called_with(
            "/provider", params={"mobile": "false", "broadband": "true"}
        )

        for p in providers:
            self.assertIn(p.name, provider_names)
