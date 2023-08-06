# -*- coding: utf-8 -*-
from ideabox.policy import _
from ideabox.policy import utils
from plone import api
from plone.app.textfield import RichText
from plone.dexterity.content import Container
from plone.supermodel import model
from Products.Five import BrowserView
from zope import schema
from zope.interface import implementer


class IStateProgress(model.Schema):
    """IStateProgress"""

    state_date = schema.Date(title=_("Date"), required=True)

    body = RichText(title=_("Content"), required=True)


@implementer(IStateProgress)
class StateProgress(Container):
    pass


class StateProgressView(BrowserView):
    def get_state_progress(self):
        return api.content.find(
            context=self.context,
            portal_type="state_progress",
            sort_on="state_date",
            sort_order="descending",
        )

    def format_date(self, value):
        return utils.localized_month(value.strftime("%d %B %Y"), self.request)
