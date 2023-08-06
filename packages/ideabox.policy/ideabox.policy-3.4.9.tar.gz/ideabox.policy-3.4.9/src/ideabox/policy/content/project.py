# -*- coding: utf-8 -*-
from Products.CMFPlone.utils import getToolByName
from collective.z3cform.select2.widget.widget import MultiSelect2FieldWidget
from ideabox.policy import _
from plone import api
from plone.app.dexterity import _ as DXMF
from plone.app.textfield import RichText
from plone.app.textfield.value import IRichTextValue
from plone.app.z3cform.widget import RichTextFieldWidget
from plone.autoform import directives as form
from plone.dexterity.browser import view
from plone.dexterity.content import Container
from plone.formwidget.geolocation.field import GeolocationField
from plone.formwidget.geolocation.interfaces import _ as _geo
from plone.indexer.decorator import indexer
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from six import text_type
from zope import schema
from zope.component import getUtility
from zope.i18n import translate
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory


class IProject(model.Schema):
    """IProject"""

    title = schema.TextLine(title=DXMF("label_title", default="Title"), required=True)

    form.widget(project_theme=MultiSelect2FieldWidget)
    project_theme = schema.List(
        title=_("Domain(s) concerned"),
        value_type=schema.Choice(
            title=_("Domain(s) concerned"), vocabulary="collective.taxonomy.theme"
        ),
        required=False,
    )

    form.widget(project_district=MultiSelect2FieldWidget)
    project_district = schema.List(
        title=_("District(s) concerned"),
        value_type=schema.Choice(
            title=_("District(s) concerned"),
            vocabulary="collective.taxonomy.district",
        ),
        required=False,
    )

    body = RichText(title=_("Content"), required=True)
    form.widget("body", RichTextFieldWidget)
    model.primary("body")

    project_image = NamedBlobImage(title=_("Project image"), required=False)

    form.mode(original_author="hidden")
    original_author = schema.TextLine(title=_("Original author"), required=False)

    geolocation = GeolocationField(
        title=_geo('label_geolocation', default=u'Geolocation'),
        description=_geo('help_geolocation',
                      default=u'Click on the map to select a location, or '
                              u'use the text input to search by address.'),
        required=False)


@implementer(IProject)
class Project(Container):
    pass


class ProjectView(view.DefaultView):

    _timeline_states = (
        "deposited",
        "project_analysis",
        "vote",
        "result_analysis",
        "study_in_progress",
        "in_progress",
        "realized",
    )
    _rating_states = ("vote", "result_analysis", "rejected")

    @property
    def can_edit(self):
        return api.user.has_permission(
            "cmf.ModifyPortalContent", obj=self.context, user=api.user.get_current()
        )

    @property
    def default_image(self):
        """Try to find the default image for the project, return `None` otherwise"""
        portal = api.portal.get()
        context = self.context
        if context.project_image is not None:
            return "{}/@@images/project_image/large".format(context.absolute_url())
        if "project_default_large.jpg" in portal:
            return portal["project_default_large.jpg"].absolute_url()

    @property
    def get_images_url(self):
        contents = self.context.listFolderContents(
            contentFilter={"portal_type": "Image"}
        )
        images_url = []
        for content in contents:
            images_url.append(content.absolute_url())
        if not images_url:
            default_image = self.default_image
            if default_image is not None:
                images_url.append(default_image)
        return images_url

    def get_news(self):
        return api.content.find(
            context=self.context,
            portal_type="News Item",
            sort_on="Date",
            sort_order="descending",
        )

    @property
    def review_state(self):
        return api.content.get_state(obj=self.context)

    @property
    def before_selected(self):
        return self.review_state in self._timeline_states[:4] + ("rejected",)

    @property
    def _workflow_history(self):
        history = [
            {
                "order": self._timeline_states.index(l.get("review_state")),
                "state": l.get("review_state"),
                "date": l.get("time"),
            }
            for l in [val for val in self.context.workflow_history.values()][0]
            if l.get("review_state") in self._timeline_states
        ]
        return sorted(history, key=lambda x: x["order"])

    @property
    def can_view_timeline(self):
        return False  # Temporarily fix as requested
        if self.review_state == "rejected":
            return False
        return self.review_state in self._timeline_states

    @property
    def can_view_rating(self):
        return self.review_state in self._rating_states

    @property
    def timeline_states(self):
        history = self._workflow_history
        current_state = self.review_state
        first_timeline_states = self._timeline_states[:4]
        second_timeline_states = self._timeline_states[4:]
        selected_states = (
            self.review_state in first_timeline_states
            and first_timeline_states
            or second_timeline_states
        )
        states = [
            {"state": e, "date": "", "class": "unfinished"} for e in selected_states
        ]
        idx = (
            current_state in self._timeline_states
            and self._timeline_states.index(current_state)
            or 0
        )
        for line in history:
            # Ensure that next steps that were completed in the past is not
            # displayed
            if line["order"] > idx:
                break
            state = [s for s in states if s["state"] == line["state"]]
            if len(state) == 1:
                state[0]["date"] = line["date"]
                state[0]["class"] = "finished"
        return states

    @property
    def anonymous(self):
        return api.user.is_anonymous()

    def creator(self):
        return getattr(self.context, "original_author", self.context.Creator())

    def author(self):
        return api.user.get(self.creator())

    def authorname(self):
        author = self.author()
        if author:
            infos = [author.getProperty("first_name"), author.getProperty("last_name")]
            return " ".join([i for i in infos if i])
        return author and author["fullname"] or self.creator()

    def get_project_theme(self):
        if not self.context.project_theme:
            return
        factory = getUtility(IVocabularyFactory, "collective.taxonomy.theme")
        vocabulary = factory(self.context)
        values = []
        for token in self.context.project_theme:
            try:
                values.append(
                    [
                        translate(
                            vocabulary.getTerm(token).title, context=self.context
                        ),
                        token,
                    ]
                ),
            except KeyError:
                continue
        site = api.portal.get().absolute_url()
        links = []
        for value in values:
            links.append(
                "<a href={0}/projets#b_start=0&c5={1}>{2}</a>".format(
                    site, value[1], value[0]
                )
            )
        return ", ".join(links)

    def get_project_district(self):
        if self.context.project_district:
            factory = getUtility(IVocabularyFactory, "collective.taxonomy.district")
            vocabulary = factory(self.context)
            values = []
            for token in self.context.project_district:
                try:
                    values.append(
                        translate(vocabulary.getTerm(token).title, context=self.context)
                    )
                except KeyError:
                    continue
            return ", ".join(values)

    def has_campaign_image(self):
        parent = self.context.aq_parent
        return parent.portal_type == "campaign" and parent.image

    def get_campaign_image(self):
        parent = self.context.aq_parent
        if parent.portal_type == "campaign" and parent.image:
            return "{0}/@@images/image".format(parent.absolute_url())
        return ""

    def is_geolocated(self):
        return is_geolocated(self.context)


@indexer(IProject)
def searchabletext_project(object, **kw):
    result = []

    fields = ["title", "description", "body", "original_author"]
    for field_name in fields:
        value = getattr(object, field_name, None)
        if type(value) is text_type:
            result.append(value)
        elif IRichTextValue.providedBy(value):
            transforms = getToolByName(object, "portal_transforms")
            text = (
                transforms.convertTo("text/plain", value.raw, mimetype=value.mimeType)
                .getData()
                .strip()
            )
            result.append(text)
        else:
            text = value
            if text:
                result.append(text)
    return " ".join(result)


def is_geolocated(obj):
    if getattr(obj, "geolocation", None) is not None:
        if (
            getattr(obj.geolocation, "latitude", None) is not None
            and getattr(obj.geolocation, "longitude", None) is not None
        ):
            if float(obj.geolocation.latitude) != float(0) and float(
                obj.geolocation.longitude
            ) != float(0):
                return True
            else:
                return False
        else:
            return False
    else:
        return False
