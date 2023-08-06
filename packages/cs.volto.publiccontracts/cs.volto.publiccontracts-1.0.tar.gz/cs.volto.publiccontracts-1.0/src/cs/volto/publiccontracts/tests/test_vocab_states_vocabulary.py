# -*- coding: utf-8 -*-
import unittest

from plone.app.testing import TEST_USER_ID, setRoles
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory, IVocabularyTokenized

from cs.volto.publiccontracts import _
from cs.volto.publiccontracts.testing import (  # noqa
    CS_VOLTO_PUBLICCONTRACTS_INTEGRATION_TESTING,
)


class StatesVocabularyIntegrationTest(unittest.TestCase):

    layer = CS_VOLTO_PUBLICCONTRACTS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_vocab_states_vocabulary(self):
        vocab_name = 'cs.volto.publiccontracts.StatesVocabulary'
        factory = getUtility(IVocabularyFactory, vocab_name)
        self.assertTrue(IVocabularyFactory.providedBy(factory))

        vocabulary = factory(self.portal)
        self.assertTrue(IVocabularyTokenized.providedBy(vocabulary))
        self.assertEqual(
            vocabulary.getTerm('sony-a7r-iii').title,
            _(u'Sony Aplha 7R III'),
        )
