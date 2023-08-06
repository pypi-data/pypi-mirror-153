from Acquisition import aq_parent
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from Products.Five import BrowserView
from collective.z3cform.datagridfield.datagridfield import DataGridFieldObjectSubForm
from ftw.referencewidget.browser.utils import get_root_path_from_source
from ftw.referencewidget.widget import ReferenceBrowserWidget
from plone.portlets.interfaces import IPortletAssignment
import json


class GeneratePathbar(BrowserView):

    def __call__(self):
        widget = self.context

        # Plone 5 tinymce integration - not a ref widget
        if not isinstance(widget, ReferenceBrowserWidget):
            widget = ReferenceBrowserWidget(self.request, allow_nonsearched_types=True)

            if IPortletAssignment.providedBy(self.context):
                widget.context = self.context.aq_parent.aq_parent
            else:
                widget.context = self.context.aq_parent

        if hasattr(self.context, 'form') and isinstance(self.context.form, DataGridFieldObjectSubForm):
            widget.context = self.context.__parent__.context

        mtool = getToolByName(widget.context, 'portal_membership')

        originpoint = self.request.get('origin', None)
        if not originpoint:
            originpoint = widget.get_start_path()

        if isinstance(originpoint, unicode):
            originpoint = originpoint.encode('utf-8')

        obj = widget.context.unrestrictedTraverse(originpoint)
        results = []

        root_path = get_root_path_from_source(widget)

        while True:
            clickable = mtool.checkPermission('View', obj)
            path = '/'.join(obj.getPhysicalPath())
            results.insert(0, {'title': obj.Title(),
                               'path': path,
                               'clickable': bool(clickable)})

            if root_path and root_path == path:
                break
            elif IPloneSiteRoot.providedBy(obj):
                break
            else:
                obj = aq_parent(obj)
        self.request.RESPONSE.setHeader("Content-type", "application/json")
        return json.dumps(results)
