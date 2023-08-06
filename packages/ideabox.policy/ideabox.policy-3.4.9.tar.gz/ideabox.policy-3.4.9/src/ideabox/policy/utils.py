# -*- coding: utf-8 -*-

from AccessControl import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from AccessControl.User import Super as BaseUnrestrictedUser
from collective.taxonomy.interfaces import ITaxonomy
from datetime import datetime
from eea.facetednavigation.layout.layout import FacetedLayout
from ideabox.policy import _
from plone import api
from plone.portlets.constants import CONTEXT_CATEGORY
from plone.portlets.interfaces import ILocalPortletAssignmentManager
from plone.portlets.interfaces import IPortletManager
from zope.component import getMultiAdapter
from zope.component import getSiteManager
from zope.component import getUtility
from zope.i18n import translate
from zope.schema.interfaces import IVocabularyFactory


class UnrestrictedUser(BaseUnrestrictedUser):
    """Unrestricted user that still has an id."""

    def getId(self):
        """Return the ID of the user."""
        return self.getUserName()


def execute_under_admin(portal, function, *args, **kwargs):
    """Execude code under admin privileges"""
    sm = getSecurityManager()
    try:
        try:
            tmp_user = UnrestrictedUser("admin", "", [""], "")
            # Wrap the user in the acquisition context of the portal
            tmp_user = tmp_user.__of__(portal.acl_users)
            newSecurityManager(None, tmp_user)
            # Call the function
            return function(*args, **kwargs)
        except:
            # If special exception handlers are needed, run them here
            raise
    finally:
        # Restore the old security manager
        setSecurityManager(sm)


def review_state(context):
    return api.content.get_state(obj=context)


def can_view_rating(context):
    _rating_states = ("vote", "result_analysis", "rejected")
    return review_state(context) in _rating_states


def now():
    return datetime.now()


def activate_faceted_navigation(context, config_path=""):
    subtyper = context.restrictedTraverse("@@faceted_subtyper")
    if subtyper.is_faceted:
        return
    subtyper.enable()
    with open(config_path, "rb") as config:
        context.unrestrictedTraverse("@@faceted_exportimport").import_xml(
            import_file=config
        )


def set_faceted_view(context, view_name):
    layout = FacetedLayout(context)
    layout.update_layout(layout=view_name)


def localized_month(value, request):
    keys = {
        "January": _("January"),
        "February": _("February"),
        "March": _("March"),
        "April": _("April"),
        "May": _("May"),
        "June": _("June"),
        "July": _("July"),
        "August": _("August"),
        "September": _("September"),
        "October": _("October"),
        "November": _("November"),
        "December": _("December"),
        "Jan": _("Jan"),
        "Feb": _("Feb"),
        "Mar": _("Mar"),
        "Apr": _("Apr"),
        "Jun": _("Jun"),
        "Jul": _("Jul"),
        "Aug": _("Aug"),
        "Sep": _("Sep"),
        "Oct": _("Oct"),
        "Nov": _("Nov"),
        "Dec": _("Dec"),
    }
    for k, v in keys.items():
        if k in value:
            value = value.replace(k, translate(v, context=request))
            return value
    return value


def disable_portlets(context, disabled=("plone.leftcolumn", "plone.rightcolumn")):
    for manager_name in disabled:
        manager = getUtility(IPortletManager, name=manager_name)
        blacklist = getMultiAdapter((context, manager), ILocalPortletAssignmentManager)
        blacklist.setBlacklistStatus(CONTEXT_CATEGORY, True)


def get_district():
    sm = getSiteManager()
    return sm.queryUtility(ITaxonomy, name="collective.taxonomy.district")


def get_theme():
    sm = getSiteManager()
    return sm.queryUtility(ITaxonomy, name="collective.taxonomy.theme")

def get_vocabulary(voc_name):
    factory = getUtility(IVocabularyFactory, voc_name)
    vocabulary = factory(api.portal.get())
    return vocabulary
