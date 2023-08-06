# -*- coding: utf-8 -*-

from eea.facetednavigation.browser.app.query import FacetedQueryHandler


class IdeaboxFacetedQueryHandler(FacetedQueryHandler):
    def query(self, *args, **kwargs):
        results = super(IdeaboxFacetedQueryHandler, self).query(*args, **kwargs)
        # Iterate over a batch breaks batch mecanisms
        # query = self.criteria()
        # if "sort_on" in query and query["sort_on"] == "random_sort":
        #     results = [e for e in results]
        #     shuffle(results)
        return results
