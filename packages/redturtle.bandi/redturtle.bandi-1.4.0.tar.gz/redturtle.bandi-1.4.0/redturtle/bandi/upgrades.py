# -*- coding: utf-8 -*-
from plone import api
from plone.app.event.base import default_timezone
from redturtle.bandi import logger

import pytz

default_profile = "profile-redturtle.bandi:default"


def update_catalog(context):
    context.runImportStepFromProfile(default_profile, "catalog")


def update_registry(context):
    context.runImportStepFromProfile(
        default_profile, "plone.app.registry", run_dependencies=False
    )


def migrate_to_1100(context):
    PROFILE_ID = "profile-redturtle.bandi:to_1100"
    context.runAllImportStepsFromProfile(PROFILE_ID)

    #  update indexes and topics
    context.runImportStepFromProfile(default_profile, "catalog")
    context.runImportStepFromProfile(
        default_profile, "plone.app.registry", run_dependencies=False
    )

    bandi = api.content.find(portal_type="Bando")
    tot_results = len(bandi)
    logger.info("### Fixing {tot} Bandi ###".format(tot=tot_results))
    for counter, brain in enumerate(bandi):
        logger.info(
            "[{counter}/{tot}] - {bando}".format(
                counter=counter + 1, tot=tot_results, bando=brain.getPath()
            )
        )
        bando = brain.getObject()
        bando.reindexObject(
            idxs=[
                "chiusura_procedimento_bando",
                "destinatari_bando",
                "scadenza_bando",
                "tipologia_bando",
            ]
        )

    criteria_mapping = {
        u"getTipologia_bando": u"tipologia_bando",
        u"getChiusura_procedimento_bando": u"chiusura_procedimento_bando",
        u"getScadenza_bando": u"scadenza_bando",
        u"getDestinatariBando": u"destinatari_bando",
    }
    collections = api.content.find(portal_type="Collection")
    tot_results = len(collections)
    logger.info("### Fixing {tot} Collections ###".format(tot=tot_results))
    for counter, brain in enumerate(collections):
        collection = brain.getObject()
        query = []
        for criteria in getattr(collection, "query", []):
            criteria["i"] = criteria_mapping.get(criteria["i"], criteria["i"])
            query.append(criteria)
        collection.query = query

        # fix sort_on
        sort_on = getattr(collection, "sort_on", "")
        if sort_on in criteria_mapping:
            collection.sort_on = criteria_mapping[sort_on]

        logger.info(
            "[{counter}/{tot}] - {collection}".format(
                counter=counter + 1,
                tot=tot_results,
                collection=brain.getPath(),
            )
        )
    logger.info("Upgrade to 3100 complete")


def migrate_to_1200(context):
    """
    Fix typo in upgrade-step
    """
    PROFILE_ID = "profile-redturtle.bandi:to_1100"
    context.runAllImportStepsFromProfile(PROFILE_ID)


def migrate_to_1300(context):
    """
    Add tzinfo to scadenza_bando
    """
    tz = pytz.timezone(default_timezone())

    bandi = api.content.find(portal_type="Bando")
    tot_results = len(bandi)
    logger.info("### Fixing {tot} Bandi ###".format(tot=tot_results))
    for counter, brain in enumerate(bandi):
        bando = brain.getObject()
        if not getattr(bando, "scadenza_bando", None):
            continue
        try:
            bando.scadenza_bando = pytz.utc.localize(bando.scadenza_bando).astimezone(
                tz
            )
        except ValueError:
            # convert to right timezone
            if bando.scadenza_bando.tzinfo.zone == tz.zone:
                # same tz, skip
                continue
            bando.scadenza_bando = pytz.utc.localize(
                bando.scadenza_bando.replace(tzinfo=None)
            ).astimezone(tz)
        bando.reindexObject(idxs=["scadenza_bando"])

        logger.info(
            "[{counter}/{tot}] - {bando}".format(
                counter=counter + 1, tot=tot_results, bando=brain.getPath()
            )
        )


def migrate_to_2000(context):
    update_catalog(context)
    update_registry(context)

    bandi = api.content.find(portal_type="Bando")
    tot_results = len(bandi)
    logger.info("### Fixing {tot} Bandi ###".format(tot=tot_results))
    for counter, brain in enumerate(bandi):
        logger.info(
            "[{counter}/{tot}] - {bando}".format(
                counter=counter + 1, tot=tot_results, bando=brain.getPath()
            )
        )
        bando = brain.getObject()
        bando.reindexObject(
            idxs=[
                "apertura_bando",
            ]
        )
