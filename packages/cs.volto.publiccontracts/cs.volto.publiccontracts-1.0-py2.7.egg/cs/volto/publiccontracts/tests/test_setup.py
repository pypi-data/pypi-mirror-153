# -*- coding: utf-8 -*-
"""Setup tests for this package."""
import unittest

from plone import api
from plone.app.testing import TEST_USER_ID, setRoles

from cs.volto.publiccontracts.testing import (  # noqa: E501
    CS_VOLTO_PUBLICCONTRACTS_INTEGRATION_TESTING,
)

try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that cs.volto.publiccontracts is properly installed."""

    layer = CS_VOLTO_PUBLICCONTRACTS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if cs.volto.publiccontracts is installed."""
        self.assertTrue(self.installer.is_product_installed(
            'cs.volto.publiccontracts'))

    def test_browserlayer(self):
        """Test that ICsVoltoPubliccontractsLayer is registered."""
        from plone.browserlayer import utils

        from cs.volto.publiccontracts.interfaces import ICsVoltoPubliccontractsLayer
        self.assertIn(
            ICsVoltoPubliccontractsLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = CS_VOLTO_PUBLICCONTRACTS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstall_product('cs.volto.publiccontracts')
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if cs.volto.publiccontracts is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed(
            'cs.volto.publiccontracts'))

    def test_browserlayer_removed(self):
        """Test that ICsVoltoPubliccontractsLayer is removed."""
        from plone.browserlayer import utils

        from cs.volto.publiccontracts.interfaces import ICsVoltoPubliccontractsLayer
        self.assertNotIn(ICsVoltoPubliccontractsLayer, utils.registered_layers())
