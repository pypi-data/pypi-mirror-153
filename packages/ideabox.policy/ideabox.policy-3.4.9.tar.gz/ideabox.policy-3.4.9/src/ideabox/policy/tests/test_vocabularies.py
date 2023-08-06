from ideabox.policy.testing import IdeaboxTestCase
from ideabox.policy.testing import IDEABOX_POLICY_INTEGRATION_TESTING
from plone import api
from zope.component import getSiteManager
from collective.taxonomy.interfaces import ITaxonomy
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID


class TestVocabularies(IdeaboxTestCase):

    layer = IDEABOX_POLICY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_vote(self):
        self.assertVocabularyLen("ideabox.vocabularies.vote", 2)

    def test_review_state(self):
        self.assertVocabularyLen("ideabox.vocabularies.review_states", 10)

    def test_gender(self):
        self.assertVocabularyLen("ideabox.vocabularies.gender", 2)

    def test_zip_code(self):
        zip_code = api.portal.get_registry_record("ideabox.vocabulary.zip_code")
        self.assertVocabularyLen("ideabox.vocabularies.zip_code", len(zip_code))
    
    def test_projects(self):
        self.assertVocabularyLen("ideabox.vocabularies.projects", 0)
        campaign = api.content.create(
            container=self.portal,
            type="campaign",
            title="Campaign1"
        )
        project = api.content.create(
            container=campaign,
            type="Project",
            title="Project1",
        )
        self.assertVocabularyLen("ideabox.vocabularies.projects", 0)
        api.content.transition(obj=project, to_state="vote")
        self.assertVocabularyLen("ideabox.vocabularies.projects", 1)
    
    def test_sort_project(self):
        self.assertVocabularyLen("ideabox.vocabularies.sort_project", 2)

    def test_district(self):
        self.assertVocabularyLen("ideabox.vocabularies.district", 4)

    def test_theme(self):
        sm = getSiteManager()
        themes = sm.queryUtility(ITaxonomy, name="collective.taxonomy.theme")
        theme_voca = themes.makeVocabulary("fr")
        self.assertVocabularyLen("ideabox.vocabularies.theme", len(theme_voca))