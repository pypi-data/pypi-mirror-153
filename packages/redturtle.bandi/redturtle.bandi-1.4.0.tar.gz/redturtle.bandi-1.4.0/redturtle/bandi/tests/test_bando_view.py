# -*- coding: utf-8 -*-
from redturtle.bandi.testing import REDTURTLE_BANDI_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class BandoViewTest(unittest.TestCase):

    layer = REDTURTLE_BANDI_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.bando = api.content.create(
            container=self.portal, type='Bando', title='Bando foo'
        )

    def test_bando_views_registered(self):
        view = api.content.get_view(
            name='bando_view', context=self.bando, request=self.request
        )
        self.assertTrue(view.__name__ == 'bando_view')

        view_right = api.content.get_view(
            name='bando_right_view', context=self.bando, request=self.request
        )
        self.assertTrue(view_right.__name__ == 'bando_right_view')

    def test_destinatari_in_view(self):
        view = api.content.get_view(
            name='bando_view', context=self.bando, request=self.request
        )
        self.assertNotIn('Recipients', view())

        bando_new = api.content.create(
            container=self.portal,
            type='Bando',
            title='Bando new',
            destinatari=['foo', 'bar'],
        )
        view_new = api.content.get_view(
            name='bando_view', context=bando_new, request=self.request
        )
        self.assertIn('Recipients', view_new())
        self.assertIn('<li>foo</li>', view_new())
        self.assertIn('<li>bar</li>', view_new())

    def test_destinatari_in_right_view(self):
        view = api.content.get_view(
            name='bando_right_view', context=self.bando, request=self.request
        )
        self.assertNotIn('Recipients', view())

        bando_new = api.content.create(
            container=self.portal,
            type='Bando',
            title='Bando new',
            destinatari=['foo', 'bar'],
        )
        view_new = api.content.get_view(
            name='bando_right_view', context=bando_new, request=self.request
        )
        self.assertIn('Recipients', view_new())
        self.assertIn('<li>foo</li>', view_new())
        self.assertIn('<li>bar</li>', view_new())

    def test_tipologia_bando_in_view(self):
        view = api.content.get_view(
            name='bando_view', context=self.bando, request=self.request
        )

        self.assertNotIn('Announcement type', view())

        bando_new = api.content.create(
            container=self.portal,
            type='Bando',
            title='Bando new',
            tipologia_bando='altro',
        )
        view_new = api.content.get_view(
            name='bando_view', context=bando_new, request=self.request
        )
        self.assertIn('Announcement type', view_new())
        self.assertIn('Altro', view_new())

    def test_tipologia_bando_in_right_view(self):
        view = api.content.get_view(
            name='bando_right_view', context=self.bando, request=self.request
        )

        self.assertNotIn('Announcement type', view())

        bando_new = api.content.create(
            container=self.portal,
            type='Bando',
            title='Bando new',
            tipologia_bando='altro',
        )
        view_new = api.content.get_view(
            name='bando_right_view', context=bando_new, request=self.request
        )
        self.assertIn('Announcement type', view_new())
        self.assertIn('Altro', view_new())
