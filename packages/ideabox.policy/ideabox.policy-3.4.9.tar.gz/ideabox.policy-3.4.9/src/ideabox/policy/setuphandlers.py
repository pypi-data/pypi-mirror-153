# -*- coding: utf-8 -*-

from Products.CMFPlone.interfaces import INonInstallable
from collective.taxonomy.exportimport import TaxonomyImportExportAdapter
from collective.taxonomy.factory import registerTaxonomy
from collective.taxonomy.interfaces import ITaxonomy
from eea.facetednavigation.layout.layout import FacetedLayout
from ideabox.policy import _
from ideabox.policy import utils
from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import queryUtility
from zope.i18n import translate
from zope.i18n.interfaces import ITranslationDomain
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory

import os


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return ["ideabox.policy:uninstall"]


def post_install(context):
    """Post install script"""
    add_taxonomies()
    portal = api.portal.get()
    if portal.get("projets") is None:
        project = api.content.create(
            type="Folder", id="projets", title="Projets", container=portal
        )
        api.content.transition(obj=project, transition="publish")
        add_behavior(
            "Folder",
            "eea.facetednavigation.subtypes.interfaces.IPossibleFacetedNavigable",
        )
        _activate_faceted_navigation(project, True, "/faceted/config/projets.xml")
        project_layout = FacetedLayout(project)
        project_layout.update_layout(layout="faceted-project")
        utils.disable_portlets(project)
        _publish(project)
    if portal.get("participer") is None:
        participate = api.content.create(
            type="Folder", id="participer", title="Participer", container=portal
        )
        utils.disable_portlets(participate)
        _publish(participate)
    if portal.get("plus-dinfos") is None:
        infos = api.content.create(
            type="Folder", id="plus-dinfos", title="Plus d'infos", container=portal
        )
        utils.disable_portlets(infos, disabled=("plone.rightcolumn",))
        _publish(infos)

    add_behavior(
        "Collection",
        "eea.facetednavigation.subtypes.interfaces.IPossibleFacetedNavigable",
    )
    if "news" in portal:
        _activate_faceted_navigation(
            portal["news"]["aggregator"], True, "/faceted/config/news.xml"
        )
        utils.disable_portlets(portal["news"])
        news_layout = FacetedLayout(portal["news"]["aggregator"])
        news_layout.update_layout(layout="faceted-news")

    allowed_sizes = api.portal.get_registry_record("plone.allowed_sizes")
    scales = ("banner 1920:800", "project_faceted 450:300", "evenement 300:300")
    for scale in scales:
        if scale not in allowed_sizes:
            allowed_sizes.append(scale)
    api.portal.set_registry_record("plone.allowed_sizes", allowed_sizes)

    api.portal.set_registry_record(
        "collective.behavior.banner.browser.controlpanel.IBannerSettingsSchema.banner_scale",
        "banner",
    )


def add_taxonomies():
    # TODO fix in test... and also in collective.taxonomy.
    current_lang = api.portal.get_current_language()[:2]

    data_theme = {
        "taxonomy": "theme",
        "field_title": translate(_("Theme"), target_language=current_lang),
        "field_description": "",
        "default_language": "fr",
        "filename": "taxonomy-settings-theme.xml",
    }

    data_district = {
        "taxonomy": "district",
        "field_title": translate(_("District (Project)"), target_language=current_lang),
        "field_description": "",
        "default_language": "fr",
        "filename": "taxonomy-settings-district.xml",
    }

    data_iam = {
        "taxonomy": "iam",
        "field_title": translate(_("I am"), target_language=current_lang),
        "field_description": "",
        "default_language": "fr",
        "filename": "taxonomy-settings-iam.xml",
    }

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
    theme_item = "collective.taxonomy.theme"
    district_item = "collective.taxonomy.district"
    iam_item = "collective.taxonomy.iam"
    locality_item = "collective.taxonomy.locality"
    utility_theme = sm.queryUtility(ITaxonomy, name=theme_item)
    utility_district = sm.queryUtility(ITaxonomy, name=district_item)
    utility_iam = sm.queryUtility(ITaxonomy, name=iam_item)
    utility_locality = sm.queryUtility(ITaxonomy, name=locality_item)

    if utility_theme and utility_district and utility_iam and utility_locality:
        return

    create_taxonomy_object(data_theme, portal)
    create_taxonomy_object(data_district, portal)
    create_taxonomy_object(data_iam, portal)
    create_taxonomy_object(data_locality, portal)

    # remove taxonomy test
    item = "collective.taxonomy.test"
    utility = sm.queryUtility(ITaxonomy, name=item)
    if utility:
        utility.unregisterBehavior()
        sm.unregisterUtility(utility, ITaxonomy, name=item)
        sm.unregisterUtility(utility, IVocabularyFactory, name=item)
        sm.unregisterUtility(utility, ITranslationDomain, name=item)


def create_taxonomy_object(data_tax, portal):
    taxonomy = registerTaxonomy(
        api.portal.get(),
        name=data_tax["taxonomy"],
        title=data_tax["field_title"],
        description=data_tax["field_description"],
        default_language=data_tax["default_language"],
    )

    adapter = TaxonomyImportExportAdapter(portal)
    data_path = os.path.join(os.path.dirname(__file__), "data")
    file_path = os.path.join(data_path, data_tax["filename"])
    with open(file_path, "r") as f:
        adapter.importDocument(taxonomy, f.read().encode("utf8"))

    del data_tax["taxonomy"]
    del data_tax["filename"]
    taxonomy.registerBehavior(**data_tax)


def add_behavior(type_name, behavior_name):
    """Add a behavior to a type"""
    fti = queryUtility(IDexterityFTI, name=type_name)
    if not fti:
        return
    behaviors = list(fti.behaviors)
    if behavior_name not in behaviors:
        behaviors.append(behavior_name)
    fti._updateProperty("behaviors", tuple(behaviors))


def _activate_faceted_navigation(context, configuration=False, path=None):
    fpath = os.path.dirname(__file__) + path
    utils.activate_faceted_navigation(context, fpath)


def _publish(obj):
    if api.content.get_state(obj) != "published":
        api.content.transition(obj, transition="publish")


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
