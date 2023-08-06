# -*- coding: utf-8 -*-

from collective.taxonomy.interfaces import ITaxonomy
from ideabox.policy import _
from ideabox.policy.utils import set_faceted_view
from ideabox.policy.setuphandlers import create_taxonomy_object
from plone import api
from plone.registry import field
from plone.registry import Record
from plone.registry.interfaces import IRegistry
from tempfile import mkstemp
from zope.component import getUtility
from zope.i18n import translate

import logging
import os

logger = logging.getLogger("ideabox.policy")


def reload_content_types(context):
    """Reload content types"""
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runImportStepFromProfile("profile-ideabox.policy:default", "typeinfo")


def fix_comments_1001(context):
    from plone.app.discussion.interfaces import IConversation

    brains = api.content.find(
        context=api.portal.get(),
        total_comments={"query": [1, 1000], "range": "min:max"},
    )
    for brain in brains:
        obj = brain.getObject()
        conversation = IConversation(obj, None)
        for thread in conversation.getThreads():
            comment = thread["comment"]
            if comment.author_name == comment.author_email:
                user = api.user.get(username=comment.author_username)
                infos = [user.getProperty("first_name"), user.getProperty("last_name")]
                comment.author_name = " ".join([i for i in infos if i])


def to_1002(context):
    """
    Fix project_district index
    """
    catalog = api.portal.get_tool("portal_catalog")
    catalog.delIndex("project_district")
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runImportStepFromProfile("profile-ideabox.policy:default", "catalog")

    for brain in api.content.find(portal_type="Project"):
        brain.getObject().reindexObject(idxs=["project_district"])


def to_1003(context):
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runImportStepFromProfile("profile-ideabox.policy:default", "viewlets")


def to_1005(context):
    """Add new tiles for priority action"""
    registry = getUtility(IRegistry)
    records = registry.records

    tiles = {
        "plone.app.mosaic.app_tiles.priorityactions": {
            "name": "ideabox.policy.priority_actions",
            "label": "Latest priority actions",
            "category": "advanced",
            "tile_type": "app",
            "default_value": "",
            "read_only": False,
            "settings": True,
            "favorite": False,
            "rich_text": False,
            "weight": 10,
        },
        "plone.app.mosaic.app_tiles.random_priorityactions": {
            "name": "ideabox.policy.random_priority_actions",
            "label": "Random priority actions",
            "category": "advanced",
            "tile_type": "app",
            "default_value": "",
            "read_only": False,
            "settings": True,
            "favorite": False,
            "rich_text": False,
            "weight": 10,
        },
    }
    types = {
        "name": (field.TextLine, "Name"),
        "label": (field.TextLine, "Label"),
        "category": (field.TextLine, "Category"),
        "tile_type": (field.TextLine, "Type"),
        "default_value": (field.TextLine, "Default value"),
        "read_only": (field.Bool, "Read only"),
        "settings": (field.Bool, "Settings"),
        "favorite": (field.Bool, "Favorite"),
        "rich_text": (field.Bool, "Rich Text"),
        "weight": (field.Int, "Weight"),
    }

    for name, values in tiles.items():
        for key, value in values.items():
            r_key = "{0}.{1}".format(name, key)
            field_type, title = types[key]
            required = True
            if key == "default_value":
                required = False
            if r_key in records:
                continue
            record = Record(field_type(title=title, required=required), value=value)
            records[r_key] = record


def to_1007(context):
    """Add new tiles for newsletter"""
    registry = getUtility(IRegistry)
    records = registry.records

    tiles = {
        "plone.app.mosaic.app_tiles.newsletter": {
            "name": "ideabox.policy.newsletter",
            "label": "Newsletter",
            "category": "advanced",
            "tile_type": "app",
            "default_value": "",
            "read_only": False,
            "settings": True,
            "favorite": False,
            "rich_text": False,
            "weight": 10,
        }
    }
    types = {
        "name": (field.TextLine, "Name"),
        "label": (field.TextLine, "Label"),
        "category": (field.TextLine, "Category"),
        "tile_type": (field.TextLine, "Type"),
        "default_value": (field.TextLine, "Default value"),
        "read_only": (field.Bool, "Read only"),
        "settings": (field.Bool, "Settings"),
        "favorite": (field.Bool, "Favorite"),
        "rich_text": (field.Bool, "Rich Text"),
        "weight": (field.Int, "Weight"),
    }

    for name, values in tiles.items():
        for key, value in values.items():
            r_key = "{0}.{1}".format(name, key)
            field_type, title = types[key]
            required = True
            if key == "default_value":
                required = False
            if r_key in records:
                continue
            record = Record(field_type(title=title, required=required), value=value)
            records[r_key] = record


def to_1008(context):
    """Add new taxonomy for locality (user profile)"""
    current_lang = api.portal.get_current_language()[:2]
    data_locality = {
        "taxonomy": "locality",
        "field_title": translate(
            _("Locality (Registration form)"), target_language=current_lang
        ),
        "field_description": "",
        "default_language": "fr",
        "filename": "taxonomy-settings-locality.xml",
    }

    portal = api.portal.get()
    sm = portal.getSiteManager()
    locality_item = "collective.taxonomy.locality"
    utility_locality = sm.queryUtility(ITaxonomy, name=locality_item)

    if not utility_locality:
        create_taxonomy_object(data_locality, portal)


def to_1009(context):
    """Add legal information text field in registry"""
    registry = getUtility(IRegistry)
    records = registry.records

    if (
        "ideabox.policy.browser.controlpanel.IIdeaBoxSettingsSchema.legal_information_text"
        in records
    ):  # noqa
        return

    logger.info(
        "Adding ideabox.policy.browser.controlpanel.IIdeaBoxSettingsSchema.legal_information_text to registry"
    )  # noqa
    record = Record(
        field.Text(
            title=_("Legal information text"),
            required=False,
            description=_("Legal information text"),
        )
    )
    records[
        "ideabox.policy.browser.controlpanel.IIdeaBoxSettingsSchema.legal_information_text"
    ] = record


def to_1010(context):
    """Add legal information text field in registry"""
    registry = getUtility(IRegistry)
    records = registry.records

    if (
        "ideabox.policy.browser.controlpanel.IIdeaBoxSettingsSchema.project_directly_submitted"
        in records
    ):  # noqa
        return

    logger.info(
        "Adding ideabox.policy.browser.controlpanel.IIdeaBoxSettingsSchema.project_directly_submitted to registry"
    )  # noqa
    record = Record(
        field.Bool(
            title=_("Projects directly submitted"),
            default=True,
            description=_(
                "If checked, projects are public as soon as they are submitted."
            ),
        )
    )
    records[
        "ideabox.policy.browser.controlpanel.IIdeaBoxSettingsSchema.project_directly_submitted"
    ] = record


def to_1011(context):
    fpath = os.path.join(os.path.dirname(__file__), "faceted", "config", "campaign.xml")
    for brain in api.content.find(portal_type="campaign"):
        obj = brain.getObject()
        xml = ""
        with open(fpath, "r") as config:
            xml = config.read()

        xml = xml.replace(
            '<property name="default">##PATH##</property>',
            '<property name="default">{0}</property>'.format(
                "/{0}".format("/".join(obj.absolute_url_path().split("/")[2:]))
            ),
        )
        fd, path = mkstemp()
        with open(path, "w") as f:
            f.write(xml)
        os.close(fd)
        with open(path, "rb") as config:
            obj.unrestrictedTraverse("@@faceted_exportimport").import_xml(
                import_file=config
            )
        set_faceted_view(obj, "faceted-project")
