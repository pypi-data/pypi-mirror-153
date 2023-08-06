# -*- coding: utf-8 -*-

from plone.api import portal as portal_api
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2
from unittest.mock import Mock
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory


import ideabox.policy
import unittest


class IdeaboxPolicyLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(name="testing.zcml", package=ideabox.policy)

    def setUpPloneSite(self, portal):
        portal.portal_workflow.setDefaultChain("simple_publication_workflow")
        portal_api.get_current_language = Mock(return_value="fr")
        applyProfile(portal, "ideabox.policy:default")


IDEABOX_POLICY_FIXTURE = IdeaboxPolicyLayer()


IDEABOX_POLICY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(IDEABOX_POLICY_FIXTURE,), name="IdeaboxPolicyLayer:IntegrationTesting"
)


IDEABOX_POLICY_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(IDEABOX_POLICY_FIXTURE,), name="IdeaboxPolicyLayer:FunctionalTesting"
)


IDEABOX_POLICY_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(IDEABOX_POLICY_FIXTURE, REMOTE_LIBRARY_BUNDLE_FIXTURE, z2.ZSERVER_FIXTURE),
    name="IdeaboxPolicyLayer:AcceptanceTesting",
)


class IdeaboxTestCase(unittest.TestCase):
    def assertVocabularyLen(self, vocname, voc_len):
        factory = getUtility(IVocabularyFactory, vocname)
        vocabulary = factory()
        self.assertEqual(len(vocabulary), voc_len)