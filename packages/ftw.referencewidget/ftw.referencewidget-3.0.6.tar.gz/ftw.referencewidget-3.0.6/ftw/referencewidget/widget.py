from Acquisition import aq_parent
from Products.CMFPlone.utils import safe_unicode
from collective.z3cform.datagridfield.datagridfield import DataGridFieldObjectSubForm
from ftw.referencewidget import _
from ftw.referencewidget.browser.utils import get_path_from_widget_start
from ftw.referencewidget.browser.utils import is_traversable
from ftw.referencewidget.interfaces import IReferenceWidget
from plone import api
from plone.app.redirector.interfaces import IRedirectionStorage
from z3c.form.browser import widget
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import IFormLayer
from z3c.form.widget import FieldWidget
from z3c.form.widget import Widget
from zope.component import adapter
from zope.component import queryUtility
from zope.i18n import translate
from zope.interface import implementer
from zope.interface import implementsOnly
from zope.schema.interfaces import IList
import json
import os


class ReferenceBrowserWidget(widget.HTMLTextInputWidget, Widget):
    """ Datepicker widget. """
    implementsOnly(IReferenceWidget)

    klass = u'reference-widget'
    request = None
    block_traversal = None
    allow_traversal = None
    selectable = None
    nonselectable = None
    start = None
    override = None

    traversal_query = None

    # Handlebar templates should not be rendered with a page templating engine,
    # because 1) <script> tags are not rendered by the zope.pagetemplate
    # implementation and 2) chameleon has troubles with handlebars.
    with open(os.path.join(os.path.dirname(__file__),
                           'templates', 'handlebars.html'), 'r') as fio:
        handlebars_html = fio.read()

    def __init__(self,
                 request,
                 block_traversal=[],
                 allow_traversal=[],
                 selectable=[],
                 nonselectable=[],
                 start='',
                 override=False,
                 allow_nonsearched_types=False,
                 traversal_query={}):
        self.request = request
        self.block_traversal = block_traversal
        self.allow_traversal = allow_traversal
        self.selectable = selectable
        self.nonselectable = nonselectable
        self.start = start
        self.override = override
        self.allow_nonsearched_types = allow_nonsearched_types
        self.traversal_query = traversal_query

    def update(self):
        super(ReferenceBrowserWidget, self).update()

        if isinstance(self.form, DataGridFieldObjectSubForm):
            self.context = self.form.__parent__.__parent__.context

        widget.addFieldClass(self)

    def is_list(self):
        if IList.providedBy(self.field):
            return 'checkbox'
        else:
            return 'radio'

    def translations(self):
        msg_search = _(u"button_seach", default="Search")
        msg_search_current_path = _(u"checkbox_search_current_path",
                                 default="Search only in current path")
        msg_close = _(u"button_close", default="Close")
        msg_sort_by = _(u"label_sort_by", default="Sort by")
        return json.dumps({'search': translate(msg_search,
                                               context=self.request),
                           'search_current_path': translate(msg_search_current_path,
                                               context=self.request),
                           'close': translate(msg_close,
                                              context=self.request),
                           'label_sort_by': translate(msg_sort_by,
                                                      context=self.request)})

    def form_url(self):
        return self.form.request.getURL()

    def current_path(self):
        return '/'.join(self.context.getPhysicalPath())

    def get_object_by_path(self, path):
        storage = queryUtility(IRedirectionStorage)

        if isinstance(path, unicode):
            path = path.encode('utf8')

        obj = self.context.unrestrictedTraverse(path, None)
        if obj is None:
            path = storage.get(path)
            obj = self.context.unrestrictedTraverse(path, None)

        return obj

    def get_items(self):
        result = []

        if not self.value:
            return

        def obj_to_dict(obj):
            return {'path': '/'.join(obj.getPhysicalPath()),
                    'title': safe_unicode(obj.Title())}

        if isinstance(self.value, list):
            for item in self.value:
                if not item:
                    continue

                obj = self.get_object_by_path(item)
                if obj:
                    result.append(obj_to_dict(obj))

        else:
            obj = self.get_object_by_path(self.value)
            if obj:
                result.append(obj_to_dict(obj))

        return result

    def get_start_path(self):
        if self.start:
            effective_path = get_path_from_widget_start(self)
        else:
            obj = self.context
            while api.portal.get() != obj and not is_traversable(self, obj):
                obj = aq_parent(obj)
            effective_path = '/'.join(obj.getPhysicalPath())
        return effective_path


@adapter(IReferenceWidget, IFormLayer)
@implementer(IFieldWidget)
def ReferenceWidgetFactory(field,
                           request,
                           block_traversal=[],
                           allow_traversal=[],
                           selectable=[],
                           nonselectable=[],
                           start='',
                           override=False,
                           allow_nonsearched_types=False,
                           traversal_query={}):
    """IFieldWidget factory for DateTimePickerWidget."""
    return FieldWidget(field, ReferenceBrowserWidget(request,
                                                     block_traversal,
                                                     allow_traversal,
                                                     selectable,
                                                     nonselectable,
                                                     start,
                                                     override,
                                                     allow_nonsearched_types,
                                                     traversal_query))
