# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from authomatic.core import User
from pas.plugins.imio.testing import PAS_PLUGINS_IMIO_FUNCTIONAL_TESTING
from plone import api

import os
import transaction
import unittest


class MockupUser:
    def __init__(self, provider, user):
        self.provider = provider
        self.provider.name = "authentic-agents"
        self.user = user
        self.user.provider = self.provider
        self.user.data = {}


class TestMigration(unittest.TestCase):
    """Test that pas.plugins.imio is properly installed."""

    layer = PAS_PLUGINS_IMIO_FUNCTIONAL_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        self.acl_users = api.portal.get_tool("acl_users")
        self.plugin = self.acl_users["authentic"]
        self.acl_users._doAddUser("jamesbond", "secret", ["Site Administrator"], [])
        transaction.commit()
        os.environ["service_ou"] = "testou"
        os.environ["service_slug"] = "testslug"
        os.environ["authentic_usagers_hostname"] = "usagers.test.be"

    # self.browser.addHeader("Authorization", "Basic jamesbond:secret")

    def test_add_existing_user(self):
        # os.environ["authentic_usagers_hostname"] = "agents.test.be"
        self.assertEqual(self.plugin.enumerateUsers(), ())
        self.assertIn("jamesbond", self.acl_users.source_users.getUserIds())
        # source_users = self.acl_users.source_users
        member = api.portal.get_tool("portal_membership").getMemberById("jamesbond")
        self.assertEqual(member.getProperty("email", ""), "")
        self.assertIn("Site Administrator", member.getRoles())
        data = {}
        data["id"] = "12345-67890"
        data["username"] = "jamesbond"
        data["email"] = "james@bond.co.uk"
        authomatic_user = User("authentic", **data)
        user = MockupUser(self.plugin, authomatic_user)
        self.plugin.remember_identity(user)
        self.assertNotIn("jamesbond", self.acl_users.source_users.getUserIds())
        new_user = self.plugin._useridentities_by_userid.get("12345-67890")
        self.assertEqual(new_user.login, "jamesbond")
        new_user = self.plugin._useridentities_by_login.get("jamesbond")
        self.assertEqual(new_user.userid, "12345-67890")
        member = api.portal.get_tool("portal_membership").getMemberById("12345-67890")
        self.assertEqual(member.getProperty("email", ""), "james@bond.co.uk")
        self.assertIn("Site Administrator", member.getRoles())

    def test_keep_owner(self):
        pass
