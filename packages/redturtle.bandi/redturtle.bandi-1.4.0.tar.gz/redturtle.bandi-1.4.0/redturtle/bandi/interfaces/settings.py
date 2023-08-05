# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope import schema
from redturtle.bandi import bandiMessageFactory as _


class IBandoSettings(Interface):
    """
    Settings used for announcements default value
    """

    default_ente = schema.Tuple(
        title=_(u"default_ente_label", default=u"Default Ente"),
        description=_(
            u"default_ente_help",
            default=u"Insert a list of default Enti that will be automatically selected when adding a new Bando.",
        ),
        required=False,
        value_type=schema.TextLine(),
        missing_value=None,
        default=(u"Regione Emilia-Romagna",),
    )

    default_destinatari = schema.Tuple(
        title=_(u"default_destinatari_label", default=u"Destinatari types"),
        description=_(
            u"default_destinatari_help",
            default=u"Insert a list of available destinatari that can be selected when adding a new Bando.",
        ),
        required=False,
        value_type=schema.TextLine(),
        missing_value=None,
        default=(
            u"Cittadini|Cittadini",
            u"Imprese|Imprese",
            u"Enti locali|Enti locali",
            u"Associazioni|Associazioni",
            u"Altro|Altro",
        ),
    )

    tipologie_bando = schema.Tuple(
        title=_("tipologie_bando_label", default=u"Announcement types"),
        description=_(
            "tipologie_help",
            u"These values will extend bandi.xml vocabulary on filesystem",
        ),
        required=False,
        value_type=schema.TextLine(),
        missing_value=None,
        default=(
            u"beni_servizi|Acquisizione beni e servizi",
            u"agevolazioni|Agevolazioni, finanziamenti, contributi",
            u"altro|Altro",
        ),
    )
