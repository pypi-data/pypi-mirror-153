from __future__ import unicode_literals  # support both Python2 and 3

from mock import patch

import unittest2 as unittest

from ..settings import REQUIRED_ENVVARS
from odoo_somconnexio_python_client.resources.crm_lead import CRMLead


@patch("odoo_somconnexio_python_client.resources.crm_lead.Client.post")
@patch.dict("os.environ", REQUIRED_ENVVARS)
class CRMLeadTests(unittest.TestCase):
    def setUp(self):
        self.address = {
            "street": "Carrer Nou",
            "zip_code": "12345",
            "city": "Barcelona",
            "country": "ES",
            "state": "B",
        }

    def test_create_mobile(self, client_post_mock):

        crm_lead_data = {
            "iban": "ESXXX",
            "subscription_request_id": 0,
            "lead_line_ids": [
                {
                    "product_code": "PRODUCT123",
                    "mobile_isp_info": {
                        "delivery_address": self.address,
                        "type": "new",
                    },
                }
            ],
        }
        expected_response_data = crm_lead_data
        expected_response_data["id"] = 1

        client_post_mock.return_value = expected_response_data

        crm_lead = CRMLead.create(**crm_lead_data)

        client_post_mock.assert_called_with("/crm-lead/create", crm_lead_data)

        lead_line_data = expected_response_data["lead_line_ids"][0]
        mobile_isp_info_data = lead_line_data["mobile_isp_info"]

        mobile_isp_info_data.pop("delivery_address")
        lead_line_data.pop("mobile_isp_info")
        expected_response_data.pop("lead_line_ids")

        lead_line = crm_lead.lead_line_ids[0]
        mobile_isp_info = lead_line.mobile_isp_info

        for key, value in expected_response_data.items():
            self.assertEqual(getattr(crm_lead, key), value)

        for key, value in lead_line_data.items():
            self.assertEqual(getattr(lead_line, key), value)

        for key, value in mobile_isp_info_data.items():
            self.assertEqual(getattr(mobile_isp_info, key), value)

    def test_create_broadband(self, client_post_mock):

        crm_lead_data = {
            "iban": "ESXXX",
            "subscription_request_id": 0,
            "lead_line_ids": [
                {
                    "product_code": "PRODUCT123",
                    "broadband_isp_info": {
                        "type": "new",
                        "delivery_address": self.address,
                        "service_address": self.address,
                    },
                }
            ],
        }
        expected_response_data = crm_lead_data
        expected_response_data["id"] = 1

        client_post_mock.return_value = expected_response_data

        crm_lead = CRMLead.create(**crm_lead_data)

        client_post_mock.assert_called_with("/crm-lead/create", crm_lead_data)

        lead_line_data = expected_response_data["lead_line_ids"][0]
        broadband_isp_info_data = lead_line_data["broadband_isp_info"]

        broadband_isp_info_data.pop("delivery_address")
        broadband_isp_info_data.pop("service_address")
        lead_line_data.pop("broadband_isp_info")
        expected_response_data.pop("lead_line_ids")

        lead_line = crm_lead.lead_line_ids[0]
        broadband_isp_info = lead_line.broadband_isp_info

        for key, value in expected_response_data.items():
            self.assertEqual(getattr(crm_lead, key), value)

        for key, value in lead_line_data.items():
            self.assertEqual(getattr(lead_line, key), value)

        for key, value in broadband_isp_info_data.items():
            self.assertEqual(getattr(broadband_isp_info, key), value)
