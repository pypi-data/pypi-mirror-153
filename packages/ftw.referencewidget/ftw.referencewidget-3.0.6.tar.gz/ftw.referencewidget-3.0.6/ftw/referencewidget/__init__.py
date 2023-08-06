from pkg_resources import get_distribution
from zope.i18nmessageid import MessageFactory


_ = MessageFactory('ftw.referencewidget')


IS_PLONE_5_OR_GREATER = get_distribution('Plone').version >= '5'


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
