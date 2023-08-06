from Products.Five.browser import BrowserView
from zExceptions import NotFound


class FakeEditView(BrowserView):
    def __call__(self):
        return NotFound
