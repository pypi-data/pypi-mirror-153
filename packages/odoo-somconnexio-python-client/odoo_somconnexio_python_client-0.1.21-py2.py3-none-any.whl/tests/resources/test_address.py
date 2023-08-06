from __future__ import unicode_literals  # support both Python2 and 3

import unittest2 as unittest

from odoo_somconnexio_python_client.resources.address import Address


class AddressTests(unittest.TestCase):
    def test_init(self):
        expected_street = "Street 123"
        expected_zip = "01345"
        expected_city = "Badalona"
        expected_state = "B"
        expected_country = "ES"

        address = Address(
            street=expected_street,
            street2="",
            zip_code=expected_zip,
            city=expected_city,
            state=expected_state,
            country=expected_country,
        )

        self.assertEqual(address.street, expected_street)
        self.assertEqual(address.street2, "")
        self.assertEqual(address.zip_code, expected_zip)
        self.assertEqual(address.city, expected_city)
        self.assertEqual(address.state, expected_state)
        self.assertEqual(address.country, expected_country)
