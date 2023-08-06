# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
    applyProfile,
)
from plone.testing import z2

import cs.volto.publiccontracts


class CsVoltoPubliccontractsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=cs.volto.publiccontracts)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'cs.volto.publiccontracts:default')


CS_VOLTO_PUBLICCONTRACTS_FIXTURE = CsVoltoPubliccontractsLayer()


CS_VOLTO_PUBLICCONTRACTS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CS_VOLTO_PUBLICCONTRACTS_FIXTURE,),
    name='CsVoltoPubliccontractsLayer:IntegrationTesting',
)


CS_VOLTO_PUBLICCONTRACTS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(CS_VOLTO_PUBLICCONTRACTS_FIXTURE,),
    name='CsVoltoPubliccontractsLayer:FunctionalTesting',
)


CS_VOLTO_PUBLICCONTRACTS_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        CS_VOLTO_PUBLICCONTRACTS_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='CsVoltoPubliccontractsLayer:AcceptanceTesting',
)
