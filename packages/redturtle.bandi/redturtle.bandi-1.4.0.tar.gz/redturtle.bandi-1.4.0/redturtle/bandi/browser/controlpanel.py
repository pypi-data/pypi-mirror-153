# -*- coding: utf-8 -*-
from plone.app.registry.browser import controlpanel
from redturtle.bandi.interfaces.settings import IBandoSettings


class BandiSettingsForm(controlpanel.RegistryEditForm):
    schema = IBandoSettings
    id = 'BandiSettingsForm'
    label = u"Impostazioni per i bandi"


class BandiControlPanel(controlpanel.ControlPanelFormWrapper):

    form = BandiSettingsForm
