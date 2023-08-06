from ideabox.policy.testing import IdeaboxTestCase
from ideabox.policy.testing import IDEABOX_POLICY_INTEGRATION_TESTING
from plone import api
from zope.component import getSiteManager
from zope.component import getUtility
from plone.registry.interfaces import IRegistry 
from plone.i18n.interfaces import ILanguageSchema
from collective.taxonomy.interfaces import ITaxonomy
from ideabox.policy.utils import can_view_rating
from ideabox.policy.utils import review_state
from ideabox.policy.utils import localized_month
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.i18n.utility import setLanguageBinding



class TestUtils(IdeaboxTestCase):

    layer = IDEABOX_POLICY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_review_state(self):
        campaign = api.content.create(
            container = self.portal,
            type="campaign",
            title="Campaign1",
        )
        project = api.content.create(
            container = campaign,
            type="Project",
            title="Project1"
        )
        api.content.transition(obj=project, to_state="vote")
        self.assertEqual(review_state(project), "vote")

    def test_localized_month(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ILanguageSchema, prefix="plone")
        settings.use_request_negotiation = True
        settings.available_languages.append("fr")
        self.request.set("HTTP_ACCEPT_LANGUAGE", "fr")
        setLanguageBinding(self.request)
        self.assertEqual(localized_month("November 2025", self.request), "Novembre 2025")
        self.assertEqual(localized_month("Kamoulox", self.request), "Kamoulox")

    def test_can_view_rating(self):
        campaign = api.content.create(
            container = self.portal,
            type="campaign",
            title="Campaign1",
        )
        project = api.content.create(
            container = campaign,
            type="Project",
            title="Project1"
        )
        api.content.transition(obj=project, to_state="project_analysis")
        self.assertFalse(can_view_rating(project))
        api.content.transition(obj=project, to_state="vote")
        self.assertTrue(can_view_rating(project))