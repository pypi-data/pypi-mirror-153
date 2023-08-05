# -*- coding: utf-8 -*-
from plone import api
from six.moves import range
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from redturtle.bandi.interfaces.settings import IBandoSettings
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


@implementer(IVocabularyFactory)
class TipologiaBandoVocabulary(object):
    def __call__(self, context):
        values = api.portal.get_registry_record(
            "tipologie_bando", interface=IBandoSettings, default=[]
        )
        terms = []
        for tipologia in values:
            key, value = tipologia.split("|")
            terms.append(SimpleTerm(value=key, token=key, title=value))
        return SimpleVocabulary(terms)


TipologiaBandoVocabularyFactory = TipologiaBandoVocabulary()


@implementer(IVocabularyFactory)
class DestinatariVocabularyFactory(object):
    def __call__(self, context):
        values = api.portal.get_registry_record(
            "default_destinatari", interface=IBandoSettings, default=[]
        )

        l = []
        for i in range(len(values)):
            l.append(tuple(values[i].split("|")))

        terms = [
            SimpleTerm(value=pair[0], token=pair[0], title=pair[1])
            for pair in l
        ]
        return SimpleVocabulary(terms)


DestinatariVocabulary = DestinatariVocabularyFactory()


@implementer(IVocabularyFactory)
class EnteVocabularyFactory(object):
    def __call__(self, context):
        catalog = api.portal.get_tool("portal_catalog")
        enti = list(catalog._catalog.uniqueValuesFor("ente_bando"))
        terms = [
            SimpleTerm(value=ente, token=ente, title=ente) for ente in enti
        ]

        return SimpleVocabulary(terms)


EnteVocabulary = EnteVocabularyFactory()
