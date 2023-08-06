# -*- coding: utf-8 -*-

from ideabox.policy import _
from plone.app.registry.browser import controlpanel
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from plone.autoform import directives as form
from z3c.form.interfaces import INPUT_MODE
from zope import schema
from zope.interface import Interface


class InvalidEmailError(schema.ValidationError):
    __doc__ = "Please enter a valid e-mail address."


class IIdeaBoxSettingsSchema(Interface):

    project_manager_email = schema.TextLine(
        title=_("Email address of the project manager"),
        description=_(
            "If there are multiple email addresses, separate them with semicolons"
        ),
    )

    form.widget("legal_information_text", klass="pat-tinymce")
    legal_information_text = schema.Text(
        title=_("Legal information text"),
        required=False,
        description=_("Legal information text"),
    )

    project_directly_submitted = schema.Bool(
        title="Projects directly submitted",
        description="If checked, projects are public as soon as they are submitted.",
        default=True,
    )


class IdeaBoxSettingsEditForm(controlpanel.RegistryEditForm):

    schema = IIdeaBoxSettingsSchema
    label = _("Configuration for ideabox product")
    description = _("")

    def updateFields(self):
        super(IdeaBoxSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(IdeaBoxSettingsEditForm, self).updateWidgets()
        self.fields["legal_information_text"].widgetFactory[
            INPUT_MODE
        ] = WysiwygFieldWidget


class IdeaBoxSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = IdeaBoxSettingsEditForm
