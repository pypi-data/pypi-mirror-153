from __future__ import unicode_literals  # support both Python2 and 3

import pytest
import unittest2 as unittest

from odoo_somconnexio_python_client.resources.product_catalog import Product, ProductCatalog


class TariffTests(unittest.TestCase):
    @pytest.mark.vcr()
    def test_search_code(self):
        pricelists = ProductCatalog.search(code="21IVA")
        tariff_names = []
        tariff_codes = []
        tariff_available_for = []

        pricelist_21IVA = pricelists[0]
        self.assertIsInstance(pricelist_21IVA, ProductCatalog)
        self.assertEqual(pricelist_21IVA.code, '21IVA')
        for product in pricelist_21IVA.products:
            self.assertIsInstance(product, Product)
            tariff_names.append(product.name)
            tariff_codes.append(product.code)
            tariff_available_for.append(product.available_for)

        self.assertIn(
            "ADSL sense fix",
            tariff_names
        )
        self.assertIn(
            "SE_SC_REC_BA_F_100",
            tariff_codes
        )
        self.assertIn(
            ["member"],
            tariff_available_for
        )

    @pytest.mark.vcr()
    def test_search_non_existant_code(self):
        pricelists = ProductCatalog.search(code="BBBB")
        self.assertEqual(len(pricelists), 0)

    @pytest.mark.vcr()
    def test_search_code_with_category_filter(self):
        pricelists = ProductCatalog.search(code="21IVA", category="mobile")
        tariff_codes = []

        pricelist_21IVA = pricelists[0]
        for product in pricelist_21IVA.products:
            tariff_codes.append(product.code)
            self.assertEqual(product.category, "mobile")

        self.assertNotIn(
            "SE_SC_REC_BA_F_100",
            tariff_codes
        )
        self.assertIn(
            "SE_SC_REC_MOBILE_T_0_0",
            tariff_codes
        )

    @pytest.mark.vcr()
    def test_search_catalog_with_lang(self):
        ca_pricelists = ProductCatalog.search(code="21IVA", lang="ca")
        es_pricelists = ProductCatalog.search(code="21IVA", lang="es")
        ca_product_names = [p.name for p in ca_pricelists[0].products]
        es_product_names = [p.name for p in es_pricelists[0].products]

        self.assertIn(
            "Il·limitades 10 GB",
            ca_product_names
        )
        self.assertIn(
            "Ilimitadas 10 GB",
            es_product_names
        )

    @pytest.mark.vcr()
    def test_search_available_products_for_product_code(self):
        """ For product fibra 100Mb only are available other Fiber products. """
        pricelists = ProductCatalog.search(product_code="SE_SC_REC_BA_F_100")
        product_codes = [p.code for p in pricelists[0].products]

        self.assertIn(
            "SE_SC_REC_BA_F_1024",
            product_codes
        )
        self.assertIn(
            "SE_SC_REC_BA_F_600",
            product_codes
        )
        self.assertNotIn(
            "SE_SC_REC_BA_ADSL_SF",
            product_codes
        )
