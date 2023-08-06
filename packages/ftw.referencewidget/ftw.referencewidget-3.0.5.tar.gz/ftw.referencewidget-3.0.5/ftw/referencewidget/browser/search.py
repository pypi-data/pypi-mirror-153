from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from ftw.referencewidget.browser.utils import extend_with_batching
from ftw.referencewidget.browser.utils import get_root_path_from_source
from ftw.referencewidget.browser.utils import get_selectable_types
from ftw.referencewidget.browser.utils import get_sort_options
from ftw.referencewidget.browser.utils import get_sort_order_options
from ftw.referencewidget.browser.utils import get_traversal_types
from ftw.referencewidget.widget import ReferenceBrowserWidget
from plone import api
from plone.portlets.interfaces import IPortletAssignment
import json


class SearchView(BrowserView):

    def __call__(self):

        widget = self.context

        # Plone 5 tinymce integration - not a ref widget
        if not isinstance(widget, ReferenceBrowserWidget):
            widget = ReferenceBrowserWidget(self.request, allow_nonsearched_types=True)

            if IPortletAssignment.providedBy(self.context):
                widget.context = self.context.aq_parent.aq_parent
            else:
                widget.context = self.context.aq_parent

        json_prep = {'items': [],
                     'sortOnOptions': get_sort_options(self.request),
                     'sortOrderOptions': get_sort_order_options(self.request)}

        uid = self.request.get('uid')
        search_term = self.request.get('term', '')
        request_path = self.request.get('request_path')
        only_current_path = self.request.get('search_current_path') == '1'
        if not search_term and not uid:
            return json.dumps(json_prep)

        if not search_term.endswith("*"):
            search_term += "*"
        search_types = get_selectable_types(widget)

        if not uid:
            query = {'portal_type': search_types,
                     'Title': search_term,
                     'sort_order': self.request.get('sort_order',
                                                    u'ascending').encode('utf-8'),
                     'sort_on': self.request.get('sort_on',
                                                 u'modified').encode('utf-8')}
            if only_current_path and request_path:
                query['path'] = request_path

            query.update(widget.traversal_query)

            root_path = get_root_path_from_source(widget)
            if root_path:
                query['path'] = root_path

        else:
            query = {'UID': uid}

        catalog = getToolByName(widget.context, 'portal_catalog')
        results = catalog(query)
        results, batch_html = extend_with_batching(widget, results)

        json_prep['batching'] = batch_html

        traversel_type = get_traversal_types(widget)
        plone = api.portal.get()
        for item in results:
            if only_current_path and request_path and item.getPath() == query['path']:
                continue

            contenttype = 'contenttype-' \
                + item.portal_type.replace('.', '-').lower()

            traversable = item.is_folderish and  \
                (item.portal_type in traversel_type)

            date = ' (%s)' % plone.toLocalizedTime(item.start) if item.start else ''

            label = '{0}{1}'.format(item.Title, date)
            if not uid:
                label += ' ({0})'.format(item.getPath())

            json_prep['items'].append({'title': label,
                                       'path': item.getPath(),
                                       'selectable': True,
                                       'uid': item.UID,
                                       'content-type': contenttype,
                                       'traversable': traversable
                                       })

        self.request.RESPONSE.setHeader("Content-type", "application/json")
        return json.dumps(json_prep)
