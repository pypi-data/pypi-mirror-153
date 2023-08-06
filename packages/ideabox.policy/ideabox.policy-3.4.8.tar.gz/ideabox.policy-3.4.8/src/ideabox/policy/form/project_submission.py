# -*- coding: utf-8 -*-

from collective.z3cform.select2.widget.widget import MultiSelect2FieldWidget
from ideabox.policy import _
from ideabox.policy import logger
from ideabox.policy.content.project import IProject
from ideabox.policy.utils import execute_under_admin
from plone import api
from z3c.form import button
from z3c.form.field import Fields
from z3c.form.form import Form
from z3c.form.interfaces import HIDDEN_MODE
from z3c.form.interfaces import IFieldsForm
from zope import schema
from zope.i18n import translate
from zope.interface import implementer


class IProjectSubmission(IProject):
    """"""


@implementer(IFieldsForm)
class ProjectSubmissionForm(Form):

    fields = Fields(IProjectSubmission).select(
        "title",
        "project_theme",
        "project_district",
        "body",
        "project_image",
        "geolocation",
        "original_author",
    )
    fields["project_theme"].widgetFactory = MultiSelect2FieldWidget
    fields["project_district"].widgetFactory = MultiSelect2FieldWidget

    fields["original_author"].mode = HIDDEN_MODE

    ignoreContext = True

    def update(self):
        super(ProjectSubmissionForm, self).update()
        self.widgets["original_author"].value = api.user.get_current().getProperty(
            "fullname"
        )

    def send_mail(self, url):
        lang = api.portal.get_current_language()[:2]

        campaign_email = self.context.emails

        if campaign_email is not None:
            list_mail = campaign_email.split(";")
        else:
            email = api.portal.get_registry_record(
                "ideabox.policy.browser.controlpanel.IIdeaBoxSettingsSchema.project_manager_email",
                default=None,
            )
            if campaign_email is None and email is None:
                logger.warn("missing email for project submission notification")
                return
            list_mail = email.split(";")

        body = translate(
            _(
                "email_body_project_submission",
                default="""A new project has been created you can access it at the following url:
              ${url}
              """,
                mapping={"url": url},
            ),
            target_language=lang,
        )
        for mail in list_mail:
            api.portal.send_email(
                recipient=mail,
                subject=translate(_("New project submission"), target_language=lang),
                body=body,
            )

    def send_request(self, data):
        context = self.context
        folder = "/".join(context.getPhysicalPath())
        if not folder.startswith("/"):
            folder = "/{0}".format(folder)
        container = api.content.get(path=folder)
        project_obj = execute_under_admin(
            container,
            api.content.create,
            type="Project",
            title=data["title"],
            project_theme=data["project_theme"],
            project_district=data["project_district"],
            body=data["body"],
            container=container,
            original_author=api.user.get_current().id,
        )
        project_directly_submitted = api.portal.get_registry_record(
            "ideabox.policy.browser.controlpanel.IIdeaBoxSettingsSchema.project_directly_submitted",
            default=True,
        )

        if project_directly_submitted is True:
            execute_under_admin(
                container, api.content.transition, obj=project_obj, transition="deposit"
            )
        if data["project_image"]:
            execute_under_admin(
                project_obj,
                api.content.create,
                type="Image",
                title=data["project_image"].filename,
                image=data["project_image"],
                container=project_obj,
            )
        self.request.response.redirect(project_obj.absolute_url())
        self.send_mail(project_obj.absolute_url())

    @button.buttonAndHandler(_("Send"), name="send")
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        self.send_request(data)
