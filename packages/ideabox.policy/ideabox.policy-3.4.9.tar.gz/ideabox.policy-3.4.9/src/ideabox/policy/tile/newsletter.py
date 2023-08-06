# -*- coding: utf-8 -*-
from ideabox.policy import _
from plone.supermodel.model import Schema
from plone.tiles import Tile
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema


class INewsletterTile(Schema):
    """A tile that displays a listing of content items"""

    title = schema.TextLine(title=_("Title"), required=True, default=_("Newsletter"))

    newsletter_link = schema.TextLine(title=_("Newsletter link"), required=True)


class NewsletterTile(Tile):
    template = ViewPageTemplateFile("templates/newsletter.pt")

    def __call__(self):
        return self.template()

    @property
    def title(self):
        return self.data.get("title") or _("Newsletter")

    @property
    def newsletter_link(self):
        return self.data.get("newsletter_link")
