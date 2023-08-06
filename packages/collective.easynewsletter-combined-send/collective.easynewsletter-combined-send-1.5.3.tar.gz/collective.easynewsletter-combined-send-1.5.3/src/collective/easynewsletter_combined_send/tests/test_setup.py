# -*- coding: utf-8 -*-
"""Setup tests for this package."""
import unittest

from collective.easynewsletter_combined_send.testing import (  # noqa: E501,
    COLLECTIVE_EASYNEWSLETTER_COMBINED_SEND_INTEGRATION_TESTING,
)
from plone import api
from plone.app.testing import TEST_USER_ID, setRoles

try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that collective.easynewsletter_combined_send is properly installed."""

    layer = COLLECTIVE_EASYNEWSLETTER_COMBINED_SEND_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.easynewsletter_combined_send is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.easynewsletter_combined_send'))

    def test_browserlayer(self):
        """Test that ICollectiveEasynewsletterCombinedSendLayer is registered."""
        from collective.easynewsletter_combined_send.interfaces import (
            ICollectiveEasynewsletterCombinedSendLayer,
        )
        from plone.browserlayer import utils
        self.assertIn(
            ICollectiveEasynewsletterCombinedSendLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_EASYNEWSLETTER_COMBINED_SEND_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['collective.easynewsletter_combined_send'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.easynewsletter_combined_send is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.easynewsletter_combined_send'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveEasynewsletterCombinedSendLayer is removed."""
        from collective.easynewsletter_combined_send.interfaces import (
            ICollectiveEasynewsletterCombinedSendLayer,
        )
        from plone.browserlayer import utils
        self.assertNotIn(
            ICollectiveEasynewsletterCombinedSendLayer,
            utils.registered_layers())
