# -*- coding: utf-8 -*-
from plone import api
from Products.Five import BrowserView
from redturtle.bandi import bandiMessageFactory as _
from zope.component import getUtility
from zope.i18n import translate
from zope.interface import implementer
from zope.interface import Interface
from zope.schema.interfaces import IVocabularyFactory


class ICollectionBandiView(Interface):
    pass


@implementer(ICollectionBandiView)
class CollectionBandiView(BrowserView):
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.voc_tipologia = getUtility(
            IVocabularyFactory, name="redturtle.bandi.tipologia.vocabulary"
        )(self.context)

    def getTipologiaTitle(self, key):
        """ """
        try:
            value = self.voc_tipologia.getTermByToken(key)
            return value.title
        except LookupError:
            return key

    def isValidDeadline(self, date):
        """ """
        if not date:
            return False
        if date.Date() == "2100/12/31":
            # a default date for bandi that don't have a defined deadline
            return False
        return True

    def getScadenzaDate(self, brain):
        date = brain.scadenza_bando
        long_format = True
        if brain.scadenza_bando.Time() == "00:00:00":
            # indexer add 1 day to this date, to make a bando ends at midnight
            # of the day-after, if time is not provided
            date = date - 1
            long_format = False
        return api.portal.get_localized_time(datetime=date, long_format=long_format)

    def getBandoState(self, brain):
        """
        return correct bando state
        """
        bando = brain.getObject()
        view = api.content.get_view(
            name="bando_view", context=bando, request=self.request
        )
        return view.getBandoState()
