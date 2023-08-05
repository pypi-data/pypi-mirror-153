# -*- coding: utf-8 -*-
from plone.app.dexterity.behaviors.metadata import IPublication
from plone.app.event.base import default_timezone
from redturtle.bandi.interfaces import IBando
from plone.restapi.deserializer.dxfields import (
    DatetimeFieldDeserializer as DefaultDatetimeFieldDeserializer,
)
from plone.restapi.interfaces import IFieldDeserializer
from pytz import timezone
from pytz import utc
from redturtle.bandi.interfaces.browserlayer import IRedturtleBandiLayer
from z3c.form.interfaces import IDataManager
from zope.component import adapter
from zope.component import queryMultiAdapter
from zope.interface import implementer
from zope.schema.interfaces import IDatetime

import dateutil
import pytz


@implementer(IFieldDeserializer)
@adapter(IDatetime, IBando, IRedturtleBandiLayer)
class DatetimeFieldDeserializer(DefaultDatetimeFieldDeserializer):
    def __call__(self, value):
        """ """
        # PATCH
        is_publication_field = self.field.interface == IPublication
        if is_publication_field:
            # because IPublication datamanager strips timezones
            tzinfo = pytz.timezone(default_timezone())
        else:
            dm = queryMultiAdapter((self.context, self.field), IDataManager)
            current = dm.get()
            if current is not None:
                tzinfo = current.tzinfo
            else:
                if self.field.getName() == "scadenza_bando":
                    tzinfo = pytz.timezone(default_timezone())
                else:
                    tzinfo = None
        # END OF PATCH

        # This happens when a 'null' is posted for a non-required field.
        if value is None:
            self.field.validate(value)
            return
        # Parse ISO 8601 string with dateutil
        try:
            dt = dateutil.parser.parse(value)
        except ValueError:
            raise ValueError(f"Invalid date: {value}")

        # Convert to TZ aware in UTC
        if dt.tzinfo is not None:
            dt = dt.astimezone(utc)
        else:
            dt = utc.localize(dt)

        # Convert to local TZ aware or naive UTC
        if tzinfo is not None:
            tz = timezone(tzinfo.zone)
            value = tz.normalize(dt.astimezone(tz))
        else:
            value = utc.normalize(dt.astimezone(utc)).replace(tzinfo=None)

        # if it's an IPublication field, remove timezone info to not break field validation
        # PATCH
        if is_publication_field:
            value = value.replace(tzinfo=None)
        # END OF PATCH
        self.field.validate(value)
        return value
