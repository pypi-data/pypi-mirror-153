# -*- coding: utf-8 -*-

from ideabox.policy import _
from plone.dexterity.content import Container
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


class ICampaign(model.Schema):
    project_submission = schema.Bool(
        title=_("Enable / Disable project submission"), default=False
    )

    emails = schema.TextLine(
        title=_("Email addresses"),
        description=_(
            'Used to send notification when a new project is proposed by an user. Accept many email addresses separated with ";"'
        ),
        required=False,
    )


@implementer(ICampaign)
class Campaign(Container):
    pass
