from Acquisition import aq_parent
from ftw.referencewidget import _
from ftw.referencewidget.browser.refbrowser_batching import RefBrowserBatchView
from ftw.referencewidget.interfaces import IReferenceSettings
from ftw.referencewidget.utils import get_types_not_searched
from plone.api import portal
from plone.batching import Batch
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope.component import getUtility
from zope.i18n import translate
from zope.schema import List


def get_traversal_types(widget):
    if widget.override and widget.allow_traversal:
        return widget.allow_traversal

    registry = getUtility(IRegistry)
    referencesettings = registry.forInterface(IReferenceSettings)
    types_not_searched = get_types_not_searched(widget.context)
    non_selectable = set()
    if not widget.allow_nonsearched_types:
        non_selectable = set(types_not_searched)
    non_selectable = non_selectable.union(
        set(referencesettings.block_traversal_additional))

    non_selectable = non_selectable.difference(
        set(referencesettings.traverse_additional))

    non_selectable = non_selectable.union(set(widget.block_traversal))
    non_selectable = non_selectable.difference(set(widget.allow_traversal))
    return remove_blacklist_from_types(widget, non_selectable)


def remove_blacklist_from_types(widget, blacklist):
    portal_types = getToolByName(widget.context, 'portal_types')
    types_to_search = portal_types.keys()
    for item in blacklist:
        if portal_types.get(item):
            types_to_search.remove(item)
    return types_to_search


def get_selectable_types_by_source(source):
    return get_selectable_types_base(source)


def get_selectable_types(widget):
    source = widget
    field = widget.field
    if isinstance(field, RelationList) or isinstance(field, List):
        value_type = getattr(field, 'value_type', None)
        if isinstance(value_type, RelationChoice):
            source = value_type.source(widget.context)
    elif isinstance(field, RelationChoice):
        source = field.source(widget.context)

    return get_selectable_types_base(source)


def get_selectable_types_base(source_or_widget):
    if source_or_widget.override and source_or_widget.selectable:
        return source_or_widget.selectable

    registry = getUtility(IRegistry)
    referencesettings = registry.forInterface(IReferenceSettings)
    non_selectable = set()
    types_not_searched = get_types_not_searched(source_or_widget.context)
    if not source_or_widget.allow_nonsearched_types:
        non_selectable = set(types_not_searched)
    non_selectable = non_selectable.union(
        set(referencesettings.block_additional))
    non_selectable = non_selectable.difference(
        set(referencesettings.select_additional))

    non_selectable = non_selectable.union(set(source_or_widget.nonselectable))
    non_selectable = non_selectable.difference(
        set(source_or_widget.selectable))
    return remove_blacklist_from_types(source_or_widget, non_selectable)


def get_path_from_widget_start(widget):
    effective_path = ""
    if not callable(widget.start):
        start = widget.start
        if (start == "parent"):
            obj = aq_parent(widget.context)
            effective_path = '/'.join(obj.getPhysicalPath())
        elif (start == "navroot"):
            obj = portal.get_navigation_root(widget.context)
            effective_path = '/'.join(obj.getPhysicalPath())
        elif (start == "ploneroot"):
            obj = portal.get()
            effective_path = '/'.join(obj.getPhysicalPath())
        else:
            effective_path = widget.start
    else:
        effective_path = widget.start(widget)
    return effective_path


def extend_with_batching(widget, results):
    page = 1
    if widget.request.get('page'):
        page = int(widget.request.get('page'))
    batch = Batch.fromPagenumber(results, pagenumber=page)
    batch_view = RefBrowserBatchView(widget, widget.request)
    return (batch, batch_view(batch, minimal_navigation=True))


def is_traversable(widget, item):

    def _is_folderish(item):

        if hasattr(item, 'is_folderish'):
            # Brainish
            return item.is_folderish
        else:
            # Assume a object
            return item.restrictedTraverse(
                '@@plone_context_state').is_folderish()

    traversel_type = get_traversal_types(widget)
    return _is_folderish(item) and  \
        (item.portal_type in traversel_type)


def get_sort_options(request):
    sort_indexes = ['', 'sortable_title', 'created', 'modified']
    options = []

    for index in sort_indexes:
        index_title = index != '' and index or 'no sort'
        options.append(
            {'title': translate(_(index_title), context=request),
             'value': index,
             'selected': index == request.get('sort_on', '')}
        )

    return options


def get_sort_order_options(request):
    sort_directions = ['ascending', 'descending']
    options = []

    for direction in sort_directions:
        options.append(
            {'title': translate(_(direction), context=request),
             'value': direction,
             'selected': direction == request.get('sort_order', '')}
        )

    return options


def get_root_path_from_source(widget):
    field = widget.field
    if isinstance(field, RelationList) or isinstance(field, List):
        value_type = getattr(field, 'value_type', None)

        if isinstance(value_type, RelationChoice):
            source = value_type.source(widget.context)
            return source.root_path

    elif isinstance(field, RelationChoice):
        source = field.source(widget.context)
        return source.root_path

    else:
        return None
