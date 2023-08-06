from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from collective.z3cform.datagridfield.datagridfield import DataGridFieldObjectSubForm
from ftw.referencewidget.browser.utils import extend_with_batching
from ftw.referencewidget.browser.utils import get_selectable_types
from ftw.referencewidget.browser.utils import get_sort_options
from ftw.referencewidget.browser.utils import get_sort_order_options
from ftw.referencewidget.browser.utils import get_traversal_types
from ftw.referencewidget.browser.utils import is_traversable
from ftw.referencewidget.widget import ReferenceBrowserWidget
from plone.portlets.interfaces import IPortletAssignment
from zope.component._api import getMultiAdapter
import json


class ReferenceJsonEndpoint(BrowserView):

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

        effective_path = widget.request.get('start', None)
        if not effective_path:
            effective_path = widget.get_start_path()
        current_depth = len(effective_path.split('/'))

        results = self.search_catalog(widget, effective_path)
        results, batch_html = extend_with_batching(widget, results)

        selectable_types = get_selectable_types(widget)

        result = {'batching': batch_html,
                  'items': [],
                  'sortOnOptions': get_sort_options(self.request),
                  'sortOrderOptions': get_sort_order_options(self.request)}

        plone = getMultiAdapter((widget.context, self.request), name="plone")
        for item in results:
            depth = len(item.getPath().split('/')) - current_depth
            if depth == 0:
                continue
            contenttype = item.portal_type.replace('.', '-').lower()

            label = item.Title or item.id
            label += ' (%s)' % plone.toLocalizedTime(item.start).encode('utf-8') if item.start else ''

            obj_dict = {'path': item.getPath(),
                        'id': item.id,
                        'uid': item.UID,
                        'title': label,
                        'folderish': item.is_folderish,
                        'traversable': is_traversable(widget, item),
                        'selectable': item.portal_type in selectable_types,
                        'content-type': 'contenttype-' + contenttype}

            result['items'].append(obj_dict)

        self.request.RESPONSE.setHeader("Content-type", "application/json")
        return json.dumps(result)

    def search_catalog(self, widget, effective_path):

        # XXX This method needs heavy refactoring
        # Also merge with the search.py

        catalog = getToolByName(widget.context, 'portal_catalog')
        selectable_types = get_selectable_types(widget)
        traversel_types = get_traversal_types(widget)

        sort_query = {
            'sort_order': self.request.get('sort_order',
                                           u'ascending').encode('utf-8'),
            'sort_on': self.request.get('sort_on', u'').encode('utf-8')}

        if not sort_query['sort_on']:
            # Show the grouped result for easier browsing
            query = {'portal_type': traversel_types,
                     'path': {'query': effective_path,
                              'depth': 1},
                     'is_folderish': True
                     }
            query.update(widget.traversal_query)

            results_folderish = catalog(query)

            query = {'portal_type': selectable_types,
                     'path': {'query': effective_path,
                              'depth': 1},
                     'is_folderish': False
                     }
            query.update(widget.traversal_query)

            results_content = catalog(query)

            folderish_selectable = set(selectable_types).difference(
                set(traversel_types))
            query = {'portal_type': list(folderish_selectable),
                     'path': {'query': effective_path,
                              'depth': 1},
                     'is_folderish': True
                     }
            query.update(widget.traversal_query)

            results_folder_select = catalog(query)
            results = results_folderish + results_content + results_folder_select

        else:
            query = {'portal_type': selectable_types + traversel_types,
                     'path': {'query': effective_path,
                              'depth': 1},
                     }
            query.update(sort_query)
            query.update(widget.traversal_query)
            results = catalog(query)

        return results
