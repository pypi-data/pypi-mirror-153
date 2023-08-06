from ftw.referencewidget.browser.utils import get_selectable_types
from ftw.referencewidget.browser.utils import get_traversal_types
from ftw.referencewidget.testing import FTW_REFERENCE_FUNCTIONAL_TESTING
from ftw.referencewidget.tests.views.form import TestView
from ftw.referencewidget.utils import get_types_not_searched
from ftw.referencewidget.utils import set_types_not_searched
from unittest import TestCase


class TestWidgetConfig(TestCase):
    layer = FTW_REFERENCE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        form = TestView(self.portal, self.portal.REQUEST)
        form.update()
        self.widget = form.form_instance.widgets['relation']
        tns = get_types_not_searched(self.portal)
        tns = tns + ('Folder',)
        set_types_not_searched(self.portal, tns)

    def test_traversable_types_more_blocked(self):
        self.widget.block_traversal = ['Document', 'Link']

        result = get_traversal_types(self.widget)
        self.assertNotIn('Document', result)
        self.assertNotIn('Link', result)

    def test_traversable_types_more_allowed(self):
        self.widget.allow_traversal = ['Folder']

        result = get_traversal_types(self.widget)
        self.assertIn('Folder', result)

    def test_selectable_types_more_allowed(self):
        self.widget.selectable = ['Folder']

        result = get_selectable_types(self.widget)
        self.assertIn('Folder', result)

    def test_selectable_types_more_blocked(self):
        self.widget.nonselectable = ['Document', 'Link']

        result = get_selectable_types(self.widget)
        self.assertTrue('Document' not in result)
        self.assertTrue('Link' not in result)
