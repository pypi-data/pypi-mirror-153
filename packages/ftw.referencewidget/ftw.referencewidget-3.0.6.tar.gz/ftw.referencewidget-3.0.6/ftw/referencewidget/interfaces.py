from zope import schema
from zope.interface import Interface
from z3c.form.interfaces import ITextWidget


class IReferenceSettings(Interface):

    select_additional = schema.Tuple(title=u"Additional types to select.",
                                     default=(),
                                     missing_value=(),
                                     value_type=schema.TextLine())

    block_additional = schema.Tuple(title=u"Additional types to block.",
                                    default=(),
                                    missing_value=(),
                                    value_type=schema.TextLine())

    traverse_additional = schema.Tuple(title=u"Additional types to traverse.",
                                       default=(),
                                       missing_value=(),
                                       value_type=schema.TextLine())

    block_traversal_additional = schema.Tuple(
        title=u"Additional types to block traversel of.", default=(),
        missing_value=(),
        value_type=schema.TextLine())


class IReferenceWidget(ITextWidget):
    """Marker interface for refwidget"""
