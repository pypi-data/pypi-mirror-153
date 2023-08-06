# -*- coding: utf-8 -*-
from Products.CMFPlone.utils import getToolByName
from ideabox.policy import _
from ideabox.policy import utils
from ideabox.policy.content.project import IProject
from ideabox.policy.content.project import Project
from ideabox.policy.content.project import ProjectView
from plone import api
from plone.app.textfield.value import IRichTextValue
from plone.indexer.decorator import indexer
from zope import schema
from zope.interface import implementer
from zope.component import queryMultiAdapter
from zope.viewlet.interfaces import IViewletManager


class IPriorityAction(IProject):
    """IPriorityActionIProject"""

    strategic_objectives = schema.TextLine(
        title=_("Strategic Objectives"), required=False
    )

    operational_objectives = schema.TextLine(
        title=_("Operational objectives"), required=False
    )


@implementer(IPriorityAction)
class PriorityAction(Project):
    pass


class PriorityActionView(ProjectView):
    def get_state_progress(self):
        return api.content.find(
            context=self.context,
            portal_type="state_progress",
            sort_on="state_date",
            sort_order="descending",
        )[:4]

    def format_date(self, value):
        return utils.localized_month(value.strftime("%d %B %Y"), self.request)

    def get_restapi_viewlets(self):
        manager = queryMultiAdapter(
            (self.context, self.request, self),
            IViewletManager,
            "plone.belowcontenttitle",
            default=None,
        )
        manager.update()
        viewlets = [v for v in manager.viewlets if v.__name__ == "imio-restapi-actions"]
        return viewlets


@indexer(IPriorityAction)
def searchabletext_priority_action(object, **kw):
    result = []

    fields = ["title", "description", "body", "original_author"]
    for field_name in fields:
        value = getattr(object, field_name, None)
        if IRichTextValue.providedBy(value):
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
