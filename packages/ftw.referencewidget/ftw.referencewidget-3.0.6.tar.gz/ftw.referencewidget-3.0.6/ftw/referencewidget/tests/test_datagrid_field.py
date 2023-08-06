from ftw.builder import Builder
from ftw.builder import create
from ftw.referencewidget.tests import FunctionalTestCase
from ftw.testbrowser import browsing


class TestDataGridField(FunctionalTestCase):

    def setUp(self):
        super(TestDataGridField, self).setUp()
        self.setup_fti(additional_behaviors=[
            'ftw.referencewidget.behaviors.IDataGridFieldExample'])
        self.grant('Manager')

    @browsing
    def test_reference_widget(self, browser):
        folder = create(Builder('folder').titled(u'Some folder'))

        content = create(Builder('refwidget sample content')
                         .titled(u'sample content'))

        browser.login().visit(content, view='@@edit')
        browser.fill({
            'The Data Grid': [
                {'Link': folder}
            ]
        }).save()

        self.assertEquals(
            [folder],
            [row['link'].to_object for row in content.the_data_grid]
        )

        browser.login().visit(content, view='@@edit')
        selected = browser.css('.selected_items [type="hidden"]')
        self.assertEquals(
            ['/plone/some-folder'],
            [node.attrib['value'] for node in selected]
        )
