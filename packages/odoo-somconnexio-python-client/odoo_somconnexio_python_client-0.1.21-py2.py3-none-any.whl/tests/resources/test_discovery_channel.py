from __future__ import unicode_literals  # support both Python2 and 3

import pytest
import unittest2 as unittest

from odoo_somconnexio_python_client.resources.discovery_channel import DiscoveryChannel


class DiscoveryChannelTests(unittest.TestCase):
    @pytest.mark.vcr()
    def test_search_default_catalan(self):
        discovery_channels = DiscoveryChannel.search()
        channel_names = []
        self.assertEqual(len(discovery_channels), 8)
        for dc in discovery_channels:
            self.assertIsInstance(dc, DiscoveryChannel)
            channel_names.append(dc.name)

        # Default lang is catalan
        self.assertIn(
            "Fires / Xerrades",
            channel_names
        )

    @pytest.mark.vcr()
    def test_search_language_spanish(self):
        discovery_channels = DiscoveryChannel.search(lang='es')
        channel_names = []
        self.assertEqual(len(discovery_channels), 8)
        for dc in discovery_channels:
            self.assertIsInstance(dc, DiscoveryChannel)
            channel_names.append(dc.name)

        self.assertIn(
            "Ferias / Charlas",
            channel_names
        )
