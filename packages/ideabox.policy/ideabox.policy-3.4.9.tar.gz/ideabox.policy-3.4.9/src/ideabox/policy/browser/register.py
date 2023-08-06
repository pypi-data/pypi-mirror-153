# -*- coding: utf-8 -*-

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ideabox.policy import _
from plone import api
from plone.app.users.browser.register import RegistrationForm
from plone.app.users.utils import notifyWidgetActionExecutionError
from z3c.form.field import Fields
from zope import schema
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer


class ICustomRegisterSchema(Interface):

    legal_conditions = schema.Bool(
        title=_("I Accept Legal terms and conditions"), required=True
    )


@adapter(Interface)
@implementer(ICustomRegisterSchema)
class CustomRegistrationAdapter(object):
    def __init__(self, context):
        self.context = context


class CustomRegistrationForm(RegistrationForm):
    template = ViewPageTemplateFile("templates/register_form.pt")

    def updateFields(self):
        super(CustomRegistrationForm, self).updateFields()
        self.fields += Fields(ICustomRegisterSchema)
        portal_url = api.portal.get().absolute_url()
        gpdr_url = "/".join([portal_url, "gdpr-view"])
        msgid = _(
            "see_legal_conditions",
            default='See <a href="${legal_conditions_url}">legal terms and conditions</a>.',
            mapping={"legal_conditions_url": gpdr_url},
        )
        legal_description = self.context.translate(msgid)
        self.fields["legal_conditions"].field.description = legal_description

    def validate_registration(self, action, data):
        super(CustomRegistrationForm, self).validate_registration(action, data)
        if not data.get("legal_conditions"):
            err_str = _("You need to accept our legal terms and conditions.")
            notifyWidgetActionExecutionError(action, "legal_conditions", err_str)
