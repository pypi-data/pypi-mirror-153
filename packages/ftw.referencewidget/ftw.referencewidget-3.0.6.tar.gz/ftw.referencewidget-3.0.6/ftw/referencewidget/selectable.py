from ftw.referencewidget.browser.utils import get_selectable_types_by_source
from zope.interface import implements
from zope.interface import Interface


class ISelectable(Interface):
    """Defines the ISelectable behavior"""

    def __init__(source, content):
        """Needs a ISource (from zope schema) and a DX content object"""

    def is_selectable():
        """"
        Return ``True`` when the object is selectable, ``False``
        when it is not selectable.
        """


class DefaultSelectable(object):
    implements(ISelectable)

    def __init__(self, source, content):
        self.source = source
        self.content = content

    def __call__(self):
        return self.is_selectable()

    def is_selectable(self):
        portal_type = self.content.portal_type
        selectable_types = get_selectable_types_by_source(self.source)

        valid_type = portal_type in selectable_types

        valid_path = True
        if self.source.root_path:
            path = '/'.join(self.content.getPhysicalPath())
            valid_path = path.startswith(self.source.root_path)

        return valid_type and valid_path
