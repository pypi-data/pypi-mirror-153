# -*- coding: utf-8 -*-

from ideabox.policy.utils import get_vocabulary
from plone.restapi.services import Service


class ThemeProjectGet(Service):
    def reply(self):
        voc_theme = get_vocabulary("ideabox.vocabularies.theme")
        result = [{"id": k, "text": v} for k, v in voc_theme.items()]
        return result


class DistrictProjectGet(Service):
    def reply(self):
        voc_district = get_vocabulary("ideabox.vocabularies.district")
        result = [{"id": k, "text": v} for k, v in voc_district.items()]
        return result
