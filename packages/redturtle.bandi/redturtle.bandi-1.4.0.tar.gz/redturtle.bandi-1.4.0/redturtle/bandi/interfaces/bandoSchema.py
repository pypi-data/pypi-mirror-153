# -*- coding: utf-8 -*-
from plone import api
from plone.app.event.base import default_timezone
from plone.app.textfield import RichText
from plone.app.z3cform.widget import AjaxSelectFieldWidget
from plone.app.z3cform.widget import DateFieldWidget
from plone.app.z3cform.widget import DatetimeFieldWidget
from plone.autoform import directives
from plone.autoform import directives as form
from plone.supermodel import model
from redturtle.bandi import bandiMessageFactory as _
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory


@provider(IContextAwareDefaultFactory)
def getDefaultEnte(context):
    default_ente = api.portal.get_registry_record(
        "redturtle.bandi.interfaces.settings.IBandoSettings.default_ente"
    )
    if default_ente:
        return default_ente
    else:
        return None


class IBandoSchema(model.Schema):
    """A Dexterity schema for Annoucements"""

    # fields
    riferimenti_bando = RichText(
        title=_("riferimenti_bando_label", default=u"References"),
        description=_("riferimenti_bando_help", default=u""),
        required=False,
    )
    apertura_bando = schema.Datetime(
        title=_("apertura_bando_label", default=u"Opening date"),
        description=_(
            "apertura_bando_help",
            default=u"Date and time of the opening of the announcement. Use "
            u"this field if you want to set a specific opening date. "
            u"If not set, the announcement will be open immediately.",
        ),
        required=False,
    )
    chiusura_procedimento_bando = schema.Date(
        title=_(
            "chiusura_procedimento_bando_label",
            default=u"Closing date procedure",
        ),
        description=_("chiusura_procedimento_bando_help", default=u""),
        required=False,
    )

    scadenza_bando = schema.Datetime(
        title=_("scadenza_bando_label", default=u"Expiration date and time"),
        description=_(
            "scadenza_bando_help",
            default=u"Deadline to participate in the announcement",
        ),
        required=False,
    )

    ente_bando = schema.Tuple(
        title=_(u"ente_label", default=u"Authority"),
        description=_(u"ente_help", default=u"Select some authorities."),
        required=False,
        defaultFactory=getDefaultEnte,
        value_type=schema.TextLine(),
        missing_value=None,
    )

    destinatari = schema.List(
        title=_("destinatari_label", default=u"Recipients"),
        description=_("destinatari_help", default=""),
        required=True,
        value_type=schema.Choice(vocabulary="redturtle.bandi.destinatari.vocabulary"),
    )

    tipologia_bando = schema.Choice(
        title=_("tipologia_bando_label", default=u"Announcement type"),
        description=_("tipologia_bando_help", default=""),
        vocabulary="redturtle.bandi.tipologia.vocabulary",
        required=True,
    )

    # order
    form.order_after(riferimenti_bando="IRichText.text")
    form.order_after(chiusura_procedimento_bando="IRichText.text")
    form.order_after(scadenza_bando="IRichText.text")
    form.order_after(ente_bando="IRichText.text")
    form.order_after(destinatari="IRichText.text")
    form.order_after(tipologia_bando="IRichText.text")

    #  widgets
    directives.widget(
        "ente_bando",
        AjaxSelectFieldWidget,
        vocabulary="redturtle.bandi.enti.vocabulary",
    )
    directives.widget(
        "apertura_bando",
        DatetimeFieldWidget,
        default_timezone=default_timezone,
    )
    directives.widget(
        "chiusura_procedimento_bando",
        DateFieldWidget,
        default_timezone=default_timezone,
    )
    directives.widget(
        "scadenza_bando",
        DatetimeFieldWidget,
        default_timezone=default_timezone,
    )
    directives.widget(destinatari=CheckBoxFieldWidget)
    directives.widget(tipologia_bando=RadioFieldWidget)
