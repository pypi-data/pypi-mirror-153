# -*- coding: utf-8 -*-
from DateTime import DateTime
from plone.indexer.decorator import indexer
from redturtle.bandi.interfaces.bando import IBando

# importo il datetime di python
from datetime import datetime

# funzione che riceve un date e torna un datetime con l'ora a zero


def dateToDatetime(d):
    return datetime.combine(d, datetime.min.time())


@indexer(IBando)
def destinatari_bando(object, **kw):
    return getattr(object, "destinatari", None)


@indexer(IBando)
def chiusura_procedimento_bando(object, **kw):

    date_chiusura_procedimento_bando = getattr(
        object, "chiusura_procedimento_bando", None
    )
    if date_chiusura_procedimento_bando:
        datetime_chiusura_procedimento_bando = dateToDatetime(
            date_chiusura_procedimento_bando
        )
    else:
        return DateTime("2100/12/31")

    if datetime_chiusura_procedimento_bando:
        return DateTime(datetime_chiusura_procedimento_bando)


@indexer(IBando)
def scadenza_bando(object, **kw):
    datetime_scadenza_bando = getattr(object, "scadenza_bando", None)
    if not datetime_scadenza_bando:
        return DateTime("2100/12/31")
    zope_dt_scadenza_bando = DateTime(datetime_scadenza_bando)
    if zope_dt_scadenza_bando.Time() == "00:00:00":
        return zope_dt_scadenza_bando + 1
    else:
        return zope_dt_scadenza_bando


@indexer(IBando)
def apertura_bando(object, **kw):
    datetime_apertura_bando = getattr(object, "apertura_bando", None)
    if not datetime_apertura_bando:
        return DateTime("1100/01/01")
    return DateTime(datetime_apertura_bando)


@indexer(IBando)
def ente_bando(object, **kw):
    return getattr(object, "ente_bando", None)


@indexer(IBando)
def tipologia_bando(object, **kw):
    return getattr(object, "tipologia_bando", None)
