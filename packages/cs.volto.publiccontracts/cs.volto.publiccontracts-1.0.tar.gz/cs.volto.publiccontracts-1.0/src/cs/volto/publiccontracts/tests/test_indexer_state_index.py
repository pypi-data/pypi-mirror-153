# -*- coding: utf-8 -*-
import unittest

from plone.app.testing import TEST_USER_ID, setRoles

from cs.volto.publiccontracts.testing import (
    CS_VOLTO_PUBLICCONTRACTS_FUNCTIONAL_TESTING,
    CS_VOLTO_PUBLICCONTRACTS_INTEGRATION_TESTING,
)


class IndexerIntegrationTest(unittest.TestCase):

    layer = CS_VOLTO_PUBLICCONTRACTS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_dummy(self):
        self.assertTrue(True)


class IndexerFunctionalTest(unittest.TestCase):

    layer = CS_VOLTO_PUBLICCONTRACTS_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_dummy(self):
        self.assertTrue(True)
