# -*- coding: utf-8 -*-
from Products.Five import BrowserView
from redturtle.bandi.interfaces.bando import IBando as newBandoInterface
from redturtle.bandi.content.bando import Bando
from redturtle.bandi.content.bandofolderdeepening import BandoFolderDeepening
from plone import api
from zope.interface import noLongerProvides
from zope.interface import alsoProvides
from redturtle.bandi.interfaces.bandofolderdeepening import (
    IBandoFolderDeepening as newFolderDeepeningInterface,
)  # noqa
from Products.CMFEditions.utilities import dereference
from BTrees.OOBTree import OOBTree
from plone.protect.interfaces import IDisableCSRFProtection


try:
    from rer.bandi.interfaces.bando import IBando as oldBandoInterface
    from rer.bandi.interfaces.bandofolderdeepening import (
        IBandoFolderDeepening as oldFolderDeepeningInterface,
    )  # noqa

    HAS_RER_BANDI = True
except ImportError:
    HAS_RER_BANDI = False

import logging

logger = logging.getLogger(__name__)


class RERMigrationView(BrowserView):
    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        if not HAS_RER_BANDI:
            return 'Impossibile eseguire la migrazione: rer.bandi non presente'
        output = ''
        brains = api.content.find(portal_type='Bando')
        logger.info('Migrating {} Bandi:'.format(len(brains)))
        output += 'Migrating {} Bandi:'.format(len(brains))
        for brain in brains:
            bando = brain.getObject()
            self.updateClass(
                obj=bando,
                className=Bando,
                oldInterface=oldBandoInterface,
                newInterface=newBandoInterface,
            )
            self.cleanHistory(obj=bando)
            subfolders = bando.listFolderContents(
                contentFilter={'portal_type': 'Bando Folder Deepening'}
            )
            logger.info('- {}'.format(brain.getPath()))
            output += '\n - {}'.format(brain.getPath())
            for subfolder in subfolders:
                self.updateClass(
                    obj=subfolder,
                    className=BandoFolderDeepening,
                    oldInterface=oldFolderDeepeningInterface,
                    newInterface=newFolderDeepeningInterface,
                )
                logger.info(
                    '  - [FOLDERDEEPENING] {}'.format(subfolder.absolute_url())
                )
                output += '\n  - [FOLDERDEEPENING] {}'.format(
                    subfolder.absolute_url()
                )

        return output

    def updateClass(self, obj, className, oldInterface, newInterface):
        parent = obj.aq_parent
        parent._delOb(obj.getId())
        obj.__class__ = className
        parent._setOb(obj.getId(), obj)
        noLongerProvides(obj, oldInterface)
        alsoProvides(obj, newInterface)
        parent[obj.getId()].reindexObject(idxs=['object_provides'])

    def cleanHistory(self, obj):
        context, history_id = dereference(obj)
        historiesstorage = api.portal.get_tool(name='portal_historiesstorage')
        history = historiesstorage._getShadowHistory(history_id)
        if not history:
            return
        keys = set(
            [
                historiesstorage._getZVCAccessInfo(history_id, selector, True)[
                    0
                ]
                for selector in history._available
            ]
        )
        versions_repo = historiesstorage._getZVCRepo()
        for key in keys:
            zope_version_history = versions_repo._histories.get(key, None)
            if zope_version_history:
                zope_version_history = OOBTree()
        storage = historiesstorage._getShadowStorage()._storage
        storage.pop(history_id, None)
        dereferenced_obj = dereference(
            history_id=history_id, zodb_hook=self.context
        )[0]
        if hasattr(dereferenced_obj, 'version_id'):
            delattr(dereferenced_obj, 'version_id')
