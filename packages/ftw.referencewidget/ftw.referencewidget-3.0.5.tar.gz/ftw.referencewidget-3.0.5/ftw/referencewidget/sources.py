from ftw.referencewidget.selectable import DefaultSelectable
from ftw.referencewidget.selectable import ISelectable
from plone import api
from Products.CMFCore.interfaces import IContentish
from zope.component.hooks import getSite
from zope.interface import implements
from zope.interface.verify import verifyClass
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.interfaces import ISource


class ReferenceObjPathSource(object):

    implements(ISource)

    def __init__(self, context, selectable_class, selectable, nonselectable,
                 override, allow_nonsearched_types, root_path):

        if not IContentish.providedBy(context):
            request = getSite().REQUEST
            nb = len(getSite().getPhysicalPath())
            if len(request.PARENTS) >= nb:
                # Workaround for data grid field.
                context = request.PARENTS[-nb]

        self.context = context
        self.selectable_class = selectable_class
        self.selectable = selectable
        self.nonselectable = nonselectable
        self.override = override
        self.allow_nonsearched_types = allow_nonsearched_types
        self.root_path = root_path

    def __contains__(self, value):
        if verifyClass(ISelectable, self.selectable_class):
            return self.selectable_class(source=self, content=value)()
        else:
            raise TypeError('Not a ISelectable class provided')


class ReferenceObjSourceBinder(object):
    implements(IContextSourceBinder)

    def __init__(self,
                 selectable_class=None,
                 selectable=None,
                 nonselectable=None,
                 override=None,
                 allow_nonsearched_types=None,
                 root_path=None):
        self.selectable_class = selectable_class or DefaultSelectable
        self.selectable = selectable or []
        self.nonselectable = nonselectable or []
        self.override = override or False
        self.allow_nonsearched_types = allow_nonsearched_types or False
        self.root_path = root_path

    def __call__(self, context):

        if not IContentish.providedBy(context):
            request = getSite().REQUEST
            nb = len(getSite().getPhysicalPath())
            if len(request.PARENTS) >= nb:
                # Workaround for data grid field.
                context = request.PARENTS[-nb]

        self.context = context
        return ReferenceObjPathSource(context,
                                      self.selectable_class,
                                      self.selectable,
                                      self.nonselectable,
                                      self.override,
                                      self.allow_nonsearched_types,
                                      self._get_root_path())

    def _get_root_path(self):
        if callable(self.root_path):
            return self.root_path(self.context)
        elif isinstance(self.root_path, basestring):
            portal_path = '/'.join(api.portal.get().getPhysicalPath())
            return portal_path + self.root_path
        else:
            return None
