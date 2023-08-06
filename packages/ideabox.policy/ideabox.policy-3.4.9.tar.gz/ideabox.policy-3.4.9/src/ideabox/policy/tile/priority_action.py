# encoding: utf-8

from hashlib import md5
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ideabox.policy import _
from ideabox.policy.faceted.subscriber import Randomizer
from plone import api
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives
from plone.supermodel.model import Schema
from plone.tiles import Tile
from random import shuffle
from zope import schema

import time


class IPriorityActionTile(Schema):
    """A tile that displays a listing of content items"""

    title = schema.TextLine(
        title=_("Title"), required=True, default=_("Priority action")
    )

    uid = schema.Choice(
        title=_("Select a container"),
        required=True,
        vocabulary="plone.app.vocabularies.Catalog",
    )
    directives.widget(
        "uid",
        RelatedItemsFieldWidget,
        pattern_options={"selectableTypes": ["campaign", "Folder"]},
    )


class TileRandomizer(Randomizer):
    def __init__(self):
        self.key = md5(str(time.time() // 60 * 5).encode("utf-8")).hexdigest()


class BasePriorityActionTile(Tile):
    template = ViewPageTemplateFile("templates/priority_action.pt")

    def __call__(self):
        return self.template()

    @property
    def title(self):
        return self.data.get("title") or _("Priority action")

    @property
    def default_image(self):
        return "{0}/project_default.jpg".format(api.portal.get().absolute_url())

    def get_contents(self, container):
        raise NotImplementedError

    def contents(self):
        uid = self.data["uid"]
        data = {"url": "", "results": []}
        if uid:
            container = api.content.get(UID=uid)
            if container:
                data["url"] = container.absolute_url()
                data["results"] = self.get_contents(container)
        return data


class LatestPriorityActionTile(BasePriorityActionTile):
    def get_contents(self, container):
        return api.content.find(
            context=container,
            portal_type="priority_action",
            sort_on="created",
            sort_order="reverse",
        )[:6]

    def folder_projects(self):
        folder = api.content.find(portal_type="Folder", id="projets")
        if len(folder) == 1:
            return folder[0].getURL()
        return False


class RandomPriorityActionTile(BasePriorityActionTile):
    def get_contents(self, container):
        query = {}
        randomizer = TileRandomizer()
        query["sort_on"] = randomizer.random_sort_key
        query["sort_order"] = randomizer.random_sort_order
        result = api.content.find(
            context=container, portal_type="priority_action", **query
        )[:200]
        shuffle(result)
        return result[:6]
