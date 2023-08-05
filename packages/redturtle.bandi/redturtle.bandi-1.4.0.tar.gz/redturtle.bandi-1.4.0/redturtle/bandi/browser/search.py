# -*- coding: utf-8 -*-
from DateTime import DateTime
from plone import api
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from six.moves.urllib.parse import quote
from zope.component import getUtility, queryUtility
from zope.schema.interfaces import IVocabularyFactory

try:
    from collective.solr.interfaces import ISolrConnectionConfig

    HAS_SOLR = True
except ImportError:
    HAS_SOLR = False

try:
    from collective.solr_collection.solr import solrUniqueValuesFor

    HAS_SOLR_COLLECTION = True
except ImportError:
    HAS_SOLR_COLLECTION = False


class SearchBandiForm(BrowserView):
    def __init__(self, context, request):
        self.context = context
        self.request = request

        voc_tipologia = getUtility(
            IVocabularyFactory, name="redturtle.bandi.tipologia.vocabulary"
        )(self.context)
        self.terms_tipologia = list(voc_tipologia)
        voc_destinatari = getUtility(
            IVocabularyFactory, name="redturtle.bandi.destinatari.vocabulary"
        )(self.context)
        self.terms_destinatari = list(voc_destinatari)
        self.solr_enabled = self.isSolrEnabled()

    def isSolrEnabled(self):
        """ """
        if not HAS_SOLR:
            return False
        util = queryUtility(ISolrConnectionConfig)
        if util:
            return getattr(util, "active", False)
        return False

    def getUniqueValuesForIndex(self, index):
        """
        get uniqueValuesFor a given index
        """
        if not self.solr_enabled or not HAS_SOLR_COLLECTION:
            pc = getToolByName(self, "portal_catalog")
            return pc.uniqueValuesFor(index)
        else:
            return solrUniqueValuesFor(index, portal_type="Bando")

    def getDefaultEnte(self):
        """
        return the default ente
        """
        portal_properties = getToolByName(self, "portal_properties")
        redturtle_bandi_settings = getattr(
            portal_properties, "redturtle_bandi_settings", None
        )
        if redturtle_bandi_settings:
            return redturtle_bandi_settings.getProperty("default_ente", "")
        return ""


class SearchBandi(BrowserView):
    """
    A view for search bandi results
    """

    def searchBandi(self):
        """
        return a list of bandi
        """
        pc = getToolByName(self.context, "portal_catalog")
        stato = self.request.form.get("stato_bandi", "")
        SearchableText = self.request.form.get("SearchableText", "")
        query = self.request.form.copy()
        if stato:
            now = DateTime()
            if stato == "scheduled":
                query["apertura_bando"] = {"query": now, "range": "min"}
            elif stato == "open":
                query["apertura_bando"] = {"query": now, "range": "max"}
                query["scadenza_bando"] = {"query": now, "range": "min"}
                query["chiusura_procedimento_bando"] = {
                    "query": now,
                    "range": "min",
                }
            elif stato == "inProgress":
                query["apertura_bando"] = {"query": now, "range": "max"}
                query["scadenza_bando"] = {"query": now, "range": "max"}
                query["chiusura_procedimento_bando"] = {
                    "query": now,
                    "range": "min",
                }
            elif stato == "closed":
                query["chiusura_procedimento_bando"] = {
                    "query": now,
                    "range": "max",
                }
        if "SearchableText" in self.request.form and not SearchableText:
            del query["SearchableText"]
        return pc(**query)

    @property
    def rss_query(self):
        """
        set rss query with the right date
        """
        query = self.request.QUERY_STRING
        stato = self.request.form.get("stato_bandi", "")
        if stato:
            now = quote(DateTime().ISO())
            if stato == "scheduled":
                query = "{query}&apertura_bando.query:record={now}&apertura_bando.range:record=min".format(
                    query=query, now=now
                )
            if stato == "open":
                query = "{query}&scadenza_bando.query:record={now}&scadenza_bando.range:record=min&chiusura_procedimento_bando.query:record={now}&chiusura_procedimento_bando.range:record=min".format(
                    query=query, now=now
                )
            elif stato == "inProgress":
                query = "{query}&amp;scadenza_bando.query:record={now}&scadenza_bando.range:record=max&amp;chiusura_procedimento_bando.query:record={now}&chiusura_procedimento_bando.range:record=min".format(
                    query=query, now=now
                )
            elif stato == "closed":
                query = "{query}&amp;chiusura_procedimento_bando.query:record={now}&chiusura_procedimento_bando.range:record=max".format(
                    query=query, now=now
                )
        return query

    def getBandoState(self, brain):
        """ """
        bando = brain.getObject()
        view = api.content.get_view(
            name="bando_view", context=bando, request=self.request
        )
        return view.getBandoState()

    def isValidDeadline(self, date):
        """ """

        if not date:
            return False
        if date.Date() == "2100/12/31":
            # a default date for bandi that don't have a defined deadline
            return False
        return True

    def getSearchResultsDescriptionLength(self):
        length = api.portal.get_registry_record(
            "plone.search_results_description_length"
        )
        return length

    def getAllowAnonymousViewAbout(self):
        return api.portal.get_registry_record("plone.allow_anon_views_about")

    def getTypesUseViewActionInListings(self):

        return api.portal.get_registry_record("plone.types_use_view_action_in_listings")
