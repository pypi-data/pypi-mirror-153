# -*- coding: utf-8 -*-
import unittest

from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import TEST_USER_ID, setRoles
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject, queryUtility

from cs.volto.publiccontracts.testing import (  # noqa
    CS_VOLTO_PUBLICCONTRACTS_INTEGRATION_TESTING,
)

try:
    from plone.dexterity.schema import portalTypeToSchemaName
except ImportError:
    # Plone < 5
    from plone.dexterity.utils import portalTypeToSchemaName


class ContractsFolderIntegrationTest(unittest.TestCase):

    layer = CS_VOLTO_PUBLICCONTRACTS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_contracts_folder_schema(self):
        fti = queryUtility(IDexterityFTI, name='ContractsFolder')
        schema = fti.lookupSchema()
        schema_name = portalTypeToSchemaName('ContractsFolder')
        self.assertIn(schema_name.lstrip('plone_0_'), schema.getName())

    def test_ct_contracts_folder_fti(self):
        fti = queryUtility(IDexterityFTI, name='ContractsFolder')
        self.assertTrue(fti)

    def test_ct_contracts_folder_factory(self):
        fti = queryUtility(IDexterityFTI, name='ContractsFolder')
        factory = fti.factory
        obj = createObject(factory)


    def test_ct_contracts_folder_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='ContractsFolder',
            id='contracts_folder',
        )


        parent = obj.__parent__
        self.assertIn('contracts_folder', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('contracts_folder', parent.objectIds())

    def test_ct_contracts_folder_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='ContractsFolder')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )

    def test_ct_contracts_folder_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='ContractsFolder')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'contracts_folder_id',
            title='ContractsFolder container',
        )
        self.parent = self.portal[parent_id]
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=self.parent,
                type='Document',
                title='My Content',
            )
