# -*- coding: utf-8 -*-

from ideabox.policy import _
from plone import schema
from plone.app.users.browser.register import BaseRegistrationForm
from plone.app.users.browser.userdatapanel import UserDataPanel
from plone.supermodel import model
from plone.z3cform.fieldsets import extensible
from z3c.form import field
from z3c.form.browser.radio import RadioFieldWidget
from zope.component import adapts
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IEnhancedUserDataSchema(model.Schema):

    last_name = schema.TextLine(title=_("Last name or institution"), required=True)

    first_name = schema.TextLine(title=_("First name"), required=False)

    address = schema.Text(title=_("Address"), required=False)

    gender = schema.Choice(
        title=_("Gender"), required=True, vocabulary="ideabox.vocabularies.gender"
    )

    birthdate = schema.Date(title=_("Birthdate"), required=True)

    zip_code = schema.Choice(
        title=_("Zip code / locality"),
        required=True,
        vocabulary="collective.taxonomy.locality",
        description=_("zip code, locality or zip code and locality"),
    )

    iam = schema.Choice(
        title=_("I am"), required=True, vocabulary="collective.taxonomy.iam"
    )


class UserDataPanelExtender(extensible.FormExtender):
    adapts(Interface, IDefaultBrowserLayer, UserDataPanel)

    def update(self):
        fields = field.Fields(IEnhancedUserDataSchema)
        fields = fields.omit("accept")
        fields["gender"].widgetFactory = RadioFieldWidget
        self.add(fields)


class RegistrationPanelExtender(extensible.FormExtender):
    adapts(Interface, IDefaultBrowserLayer, BaseRegistrationForm)

    def update(self):
        fields = field.Fields(IEnhancedUserDataSchema)
        fields["gender"].widgetFactory = RadioFieldWidget
        self.add(fields)
