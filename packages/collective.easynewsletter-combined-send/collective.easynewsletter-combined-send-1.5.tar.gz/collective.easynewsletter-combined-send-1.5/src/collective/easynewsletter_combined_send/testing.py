# -*- coding: utf-8 -*-
import collective.easynewsletter_combined_send
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
    applyProfile,
)
from plone.testing import z2
from Products.CMFCore.utils import getToolByName
from zope.configuration import xmlconfig


class CollectiveEasynewsletterCombinedSendLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.

        import Products.EasyNewsletter
        self.loadZCML(package=Products.EasyNewsletter)

        import plone.app.multilingual
        xmlconfig.file('testing.zcml', plone.app.multilingual,
                       context=configurationContext)
        xmlconfig.file('overrides.zcml', plone.app.multilingual,
                       context=configurationContext)

        self.loadZCML(package=collective.easynewsletter_combined_send)
        xmlconfig.file(
            "overrides.zcml",
            collective.easynewsletter_combined_send,
            context=configurationContext,
        )
        # z2.installProduct(app, "plone.app.contenttypes")
        # z2.installProduct(app, "Products.EasyNewsletter")

    def setUpPloneSite(self, portal):
        language_tool = getToolByName(portal, "portal_languages")
        language_tool.addSupportedLanguage("en")
        language_tool.addSupportedLanguage("de")
        applyProfile(portal, "plone.app.multilingual:default")
        applyProfile(portal, "Products.EasyNewsletter:default")
        applyProfile(portal, "collective.easynewsletter_combined_send:default")
        # Set default workflow
        wftool = getToolByName(portal, 'portal_workflow')
        wftool.setDefaultChain('simple_publication_workflow')


COLLECTIVE_EASYNEWSLETTER_COMBINED_SEND_FIXTURE = CollectiveEasynewsletterCombinedSendLayer()


COLLECTIVE_EASYNEWSLETTER_COMBINED_SEND_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_EASYNEWSLETTER_COMBINED_SEND_FIXTURE,),
    name="CollectiveEasynewsletterCombinedSendLayer:IntegrationTesting",
)


COLLECTIVE_EASYNEWSLETTER_COMBINED_SEND_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_EASYNEWSLETTER_COMBINED_SEND_FIXTURE,),
    name="CollectiveEasynewsletterCombinedSendLayer:FunctionalTesting",
)


COLLECTIVE_EASYNEWSLETTER_COMBINED_SEND_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_EASYNEWSLETTER_COMBINED_SEND_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name="CollectiveEasynewsletterCombinedSendLayer:AcceptanceTesting",
)
