from ftw.builder import Builder
from ftw.builder import create
from ftw.referencewidget.converter import ReferenceDataListConverter
from ftw.referencewidget.testing import FTW_REFERENCE_FUNCTIONAL_TESTING
from ftw.referencewidget.tests.views.form import TestView
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from unittest import TestCase


class TestFieldConverter(TestCase):
    layer = FTW_REFERENCE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.folder = create(Builder('folder'))
        self.file1 = create(Builder('file').within(self.folder))
        self.file2 = create(Builder('file'))
        form = TestView(self.portal, self.portal.REQUEST)
        form.update()
        widget = form.form_instance.widgets['relation']
        self.converter = ReferenceDataListConverter(widget.field, widget)

    def test_widget_to_field(self):
        payload = ['/'.join(self.folder.getPhysicalPath()),
                   '/'.join(self.file2.getPhysicalPath())]
        result = self.converter.toFieldValue(payload)
        self.assertEquals(self.folder, result[0])
        self.assertEquals(self.file2, result[1])

    def test_field_to_widget(self):
        expected = ['/'.join(self.folder.getPhysicalPath()),
                    '/'.join(self.file2.getPhysicalPath())]
        payload = [self.folder, self.file2]
        result = self.converter.toWidgetValue(payload)
        self.assertEquals(expected[0], result[0])
        self.assertEquals(expected[1], result[1])
