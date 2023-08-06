# -*- coding: utf-8 -*-

from ideabox.policy.form.project_submission import ProjectSubmissionForm
from plone import api
from plone.z3cform.layout import FormWrapper
from ideabox.policy.browser.controlpanel import IIdeaBoxSettingsSchema


class ProjectSubmissionView(FormWrapper):
    form = ProjectSubmissionForm

    def enable_submission(self):
        context = self.context
        return context.project_submission

    def legal_information_text(self):
        text = api.portal.get_registry_record(
            name="legal_information_text",
            interface=IIdeaBoxSettingsSchema,
            default="",
        )
        return text
