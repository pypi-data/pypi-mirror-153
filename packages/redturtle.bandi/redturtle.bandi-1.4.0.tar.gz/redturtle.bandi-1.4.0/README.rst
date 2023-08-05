Introduction
============

redturtle.bandi is a product for announcements based on 3.x branch of `rer.bandi`__.

__ http://pypi.python.org/pypi/rer.bandi


It allows to set some infos about the announcement like the deadline to participate or the closing date.


Migration from rer.bandi
========================

If you need to migrate rer.bandi -> redturtle.bandi, follow these instructions:

- Copy bandi settings somewhere
- Add both products in the buildout
- Uninstall rer.bandi
- Install redturtle.bandi
- Fill Bandi control panel with old settings
- Call "migration-from-rer" view on the Plone site root (this view will change the base classe of already created Bando and Folder Deepening items, and clean history)
- Remove rer.bandi from buildout


Composition
===========

Different layouts
-----------------
There are two allowed views for an announcement:

* default view, with basic infos on the right (like events) and extra infos (folder deepenings) in the middle.
* alternative view that moves extra infos slot below basic infos.

Folder deepening
----------------
Like in **rer.structured_content**, it has a special folder type called "*Folder Deepening*" that allows to manage some extra infos or attachment that should be shown in the announcement's view.

Topic criterias
---------------
There are some new topic criterias that allows to set topic queries for announcements.

Announcements search
--------------------
There is a search form (http://yoursite/search_bandi_form) for quick searches.

Announcement state information
------------------------------
In the search results and in the two new topic views, there are also some infos about the announcement, like his state (open, closed or in progress).

Announcements portlet
---------------------
There is also a portlet that show announcement infos from a topic (this portlet extends base collection portlet)


Configurations
==============
An announcement has some fields for set the announcement type and recipients.

Available values are set in "Bandi Settings" control panel.


Authority Default value
-----------------------

A default authority value can be set for announcements. This information is taken from control panel "Bandi Settings" (default_ente).

If the property is empty, the default value isn't set.

Tile
====

In order to use layout bandi for tile is necessary have installed collective.tiles.collection product.

plone.restapi integrations
==========================

Controlpanel
------------

Bandi controlpanel is also exposed via restapi to allow Volto integration.


DateTime fields deserializer
----------------------------

There is a custom deserializer for DateTime fields to set the right timezone when saving these fields (like start and end in Events).


Dependencies
============

This product has been tested on Plone 5.2


Credits
=======

Developed with the support of `Regione Emilia Romagna`__;

Regione Emilia Romagna supports the `PloneGov initiative`__.

__ http://www.regione.emilia-romagna.it/
__ http://www.plonegov.it/

Authors
=======

This product was developed by RedTurtle Technology team.

.. image:: http://www.redturtle.net/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.net/
