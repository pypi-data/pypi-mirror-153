from datetime import datetime
from ftw.builder import Builder
from ftw.builder import create
from ftw.referencewidget import IS_PLONE_5_OR_GREATER
from ftw.referencewidget.browser.search import SearchView
from ftw.referencewidget.testing import FTW_REFERENCE_FUNCTIONAL_TESTING
from ftw.referencewidget.tests import FunctionalTestCase
from ftw.referencewidget.tests.views.form import TestView
from ftw.testing.freezer import freeze
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from unittest import TestCase
import json


class TestSearchView(TestCase):
    layer = FTW_REFERENCE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.folder = create(Builder('folder').titled(u'Testfolder'))
        self.lower_file = create(Builder('file').within(
            self.folder).titled(u'Test'))
        self.file = create(Builder('file').titled("Sch\xc3\xbctzenpanzer"))
        form = TestView(self.portal, self.portal.REQUEST)
        form.update()
        self.widget = form.form_instance.widgets['relation']

    def test_search_view(self):
        self.widget.request['term'] = 'tes'
        self.widget.request['sort_on'] = 'sortable_title'
        view = SearchView(self.widget, self.widget.request)
        result = view()
        results = json.loads(result)
        items = results['items']
        self.assertEquals(2, len(items))
        self.assertEquals("/plone/testfolder", items[1]['path'])
        self.assertEquals("Testfolder (/plone/testfolder)", items[1]['title'])

        self.assertEquals("/plone/testfolder/test", items[0]['path'])
        self.assertEquals("Test (/plone/testfolder/test)", items[0]['title'])

    def test_search_only_from_current_path(self):
        create(Builder('file').titled('Test File - not in search results'))

        self.widget.request['term'] = 'tes'
        self.widget.request['sort_on'] = 'sortable_title'
        self.widget.request['search_current_path'] = '1'
        self.widget.request['request_path'] = '/'.join(self.folder.getPhysicalPath())

        view = SearchView(self.widget, self.widget.request)
        result = view()
        results = json.loads(result)
        items = results['items']
        self.assertEquals(1, len(items))
        self.assertEquals("Test (/plone/testfolder/test)", items[0]['title'])

    def test_search_view_on_news(self):
        with freeze(datetime(2017, 10, 4)):
            create(Builder('event').within(self.folder).titled(u'Event'))
        self.widget.request['term'] = 'Event'
        self.widget.request['sort_on'] = 'sortable_title'
        view = SearchView(self.widget, self.widget.request)
        result = view()
        results = json.loads(result)
        items = results['items']
        self.assertEquals(1, len(items))
        self.assertEquals(u'/plone/testfolder/event', items[0]['path'])
        self.assertEquals(u'Event (Oct 04, 2017) (/plone/testfolder/event)',
                          items[0]['title'])

    def test_only_correct_types(self):
        self.widget.override = True
        self.widget.selectable = ["Folder"]
        self.widget.request['term'] = 'tes'
        view = SearchView(self.widget, self.widget.request)
        result = view()
        results = json.loads(result)
        items = results['items']
        self.assertEquals(1, len(items))
        self.assertEquals("/plone/testfolder", items[0]['path'])
        self.assertEquals("Testfolder (/plone/testfolder)", items[0]['title'])

    def test_additional_traversable_query_is_applied(self):
        create(Builder('file').titled(u'testfile'))

        self.widget.request['term'] = 'tes'
        self.widget.request['sort_on'] = 'sortable_title'

        if IS_PLONE_5_OR_GREATER:
            from plone.dexterity.interfaces import IDexterityContainer
            self.widget.traversal_query = {
                'object_provides': [IDexterityContainer.__identifier__]}
        else:
            from Products.ATContentTypes.interfaces.folder import IATFolder
            self.widget.traversal_query = {
                'object_provides': [IATFolder.__identifier__]}

        result = json.loads(SearchView(
            self.widget, self.widget.request)())['items']

        self.assertEquals(1, len(result), 'Exepct only one item')
        self.assertEquals('/plone/testfolder', result[0]['path'])


class TestSearchWithPathRestriction(FunctionalTestCase):

    def setUp(self):
        super(TestSearchWithPathRestriction, self).setUp()
        self.setup_fti(additional_behaviors=[
            'ftw.referencewidget.behaviors.IRelationChoiceRestricted'])
        self.grant('Manager')

    def test_root_path_restriction_of_source_is_respected(self):
        testfolder = create(Builder('folder')
                            .titled(u'testfolder'))
        subfolder = create(Builder('folder')
                           .within(testfolder)
                           .titled(u'Some folder'))
        content = create(Builder('refwidget sample content')
                         .within(subfolder)
                         .titled(u'Some folder'))

        other_folder = create(Builder('folder').titled(u'Other folder'))

        self.portal.REQUEST['term'] = 'folde'
        result = self._get_search_result_from_widget(
            content,
            'IRelationChoiceRestricted.realtionchoice_restricted_path')

        self.assertEquals(2, len(result['items']))
        self.assertNotIn(other_folder.Title(),
                         [item['title'] for item in result['items']])

    def _get_search_result_from_widget(self, source, name):
        form = source.unrestrictedTraverse('@@edit').form_instance
        form.update()
        widget = form.widgets[name]
        return json.loads(SearchView(widget, widget.request)())
