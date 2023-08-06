from __future__ import unicode_literals  # support both Python2 and 3

from mock import patch

import unittest2 as unittest

from ..settings import REQUIRED_ENVVARS
from odoo_somconnexio_python_client.resources.subscription_request import (
    SubscriptionRequest,
)


@patch.dict("os.environ", REQUIRED_ENVVARS)
class SubscriptionRequestTests(unittest.TestCase):
    @patch("odoo_somconnexio_python_client.resources.subscription_request.Client.post")
    def test_create(self, client_post_mock):

        subscription_request_data = {
            "name": "Didac",
            "surname": "Grau Nols",
            "email": "didac.gn@test.coop",
            "ordered_parts": 0,
            "address": {
                "street": "Street 123",
                "zip_code": "01345",
                "city": "Badalona",
                "state": "B",
                "country": "ES",
            },
            "lang": "es_CA",
            "discovery_channel_id": 4,
            "share_product": 0,
            "iban": "ES6621000418401234567891",
            "vat": "73420857G",
            "coop_agreement": "",
            "voluntary_contribution": "",
            "nationality": "ES",
            "payment_type": "",
        }
        expected_response_data = {
            "id": 1,
            "name": "Didac",
            "surname": "Grau Nols",
            "email": "didac.gn@test.coop",
            "ordered_parts": 0,
            "address": {
                "street": "Street 123",
                "zip_code": "01345",
                "city": "Badalona",
                "state": "B",
                "country": "ES",
            },
            "lang": "es_CA",
            "share_product": 0,
            "iban": "ES6621000418401234567891",
            "vat": "73420857G",
            "coop_agreement": "",
            "voluntary_contribution": "",
            "nationality": "ES",
            "payment_type": "",
        }

        client_post_mock.return_value = expected_response_data

        subscription_request = SubscriptionRequest.create(**subscription_request_data)

        address_data = expected_response_data["address"]
        expected_response_data.pop("address")

        for key, value in expected_response_data.items():
            self.assertEqual(getattr(subscription_request, key), value)
        for key, value in address_data.items():
            self.assertEqual(getattr(subscription_request.address, key), value)

        client_post_mock.assert_called_with(
            "/subscription-request/create", subscription_request_data
        )
