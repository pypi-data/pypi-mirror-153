from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from collective.tiles.collection.interfaces import (
    ICollectiveTilesCollectionLayer,
)


class IRedturtleBandiLayer(
    IDefaultBrowserLayer, ICollectiveTilesCollectionLayer
):
    """Marker interface that defines a browser layer."""
