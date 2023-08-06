# -*- coding: utf-8 -*-

from eea.facetednavigation.widgets import ViewPageTemplateFile
from eea.facetednavigation.widgets.widget import Widget as AbstractWidget
from ideabox.policy import _
from zope import schema
from z3c.form import field
from eea.facetednavigation.widgets.interfaces import ISchema
from eea.facetednavigation.widgets.interfaces import LayoutSchemata
from eea.facetednavigation.widgets.interfaces import DefaultSchemata as DS
from eea.facetednavigation import EEAMessageFactory as EEAMF_


class IProjectSortingSchema(ISchema):
    vocabulary = schema.Choice(
        title=EEAMF_("Filter from vocabulary"),
        description=EEAMF_(
            "Vocabulary to use to filter sorting criteria. "
            "Leave empty for default sorting criteria."
        ),
        vocabulary="eea.faceted.vocabularies.PortalVocabularies",
        required=True,
    )


class DefaultSchemata(DS):
    """Schemata default"""

    fields = field.Fields(IProjectSortingSchema).select(
        "title", "vocabulary", "default"
    )


class Widget(AbstractWidget):
    """Widget"""

    widget_type = "project_sorting"
    widget_label = _("Project Sorting")

    groups = (DefaultSchemata, LayoutSchemata)
    index = ViewPageTemplateFile("project_sorting_widget.pt")

    @property
    def css_class(self):
        """Widget specific css class"""
        base = super(Widget, self).css_class
        return "faceted-sorting-widget {0}".format(base)

    @property
    def default(self):
        """Return default sorting values"""
        default = self.data.get("default", "")
        if not default:
            return ()
        reverse = False
        if "(reverse)" in default:
            default = default.replace("(reverse)", "", 1)
            reverse = True
        default = default.strip()
        return (default, reverse)

    def query(self, form):
        """Get value from form and return a catalog dict query"""
        query = {}

        if self.hidden:
            default = self.default
            sort_on = default[0] if default else None
            reverse = default[1] if len(default) > 1 else False
        else:
            sort_on = form.get(self.data.getId(), "")
            reverse = form.get("reversed", False)

        if sort_on:
            query["sort_on"] = sort_on

        if reverse:
            query["sort_order"] = "descending"
        else:
            query["sort_order"] = "ascending"

        return query

    def validateAddCriterion(self, indexId, criteriaType):
        """Is criteriaType acceptable criteria for indexId"""
        return True

    def vocabulary(self, **kwargs):
        """Return data vocabulary"""
        vocab = self.portal_vocabulary()
        vocab_fields = [(x[0].replace("term.", "", 1), x[1], "") for x in vocab]
        return vocab_fields
