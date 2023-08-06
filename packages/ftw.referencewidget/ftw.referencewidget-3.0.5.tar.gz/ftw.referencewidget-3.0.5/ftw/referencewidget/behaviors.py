from collective.z3cform.datagridfield.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.row import DictRow
from ftw.referencewidget.selectable import DefaultSelectable
from ftw.referencewidget.sources import ReferenceObjSourceBinder
from ftw.referencewidget.widget import ReferenceWidgetFactory
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from plone.supermodel.model import fieldset
from Products.CMFPlone import PloneMessageFactory as _
from z3c.relationfield.schema import RelationChoice, RelationList
from zope import schema
from zope.interface import alsoProvides
from zope.interface import Interface


class IRelatedItems(Interface):
    """Behavior, which provides the same functionality as the
    plone.app.relationfield IRelatedItems behavior, BUT it uses a different
    widget.

    """

    fieldset('categorization',
             label=_(u'Categorization'),
             fields=['relatedItems'])

    directives.widget(relatedItems=ReferenceWidgetFactory)
    relatedItems = RelationList(
        title=_(u'label_related_items', default=u'Related Items'),
        default=[],
        value_type=RelationChoice(title=u"Related",
                                  source=ReferenceObjSourceBinder()),
        required=False,
    )

alsoProvides(IRelatedItems, IFormFieldProvider)


class IRelationChoiceExample(Interface):
    """Demo behavior containing a RelationChoice (single value).

    """
    directives.widget(realtionchoice=ReferenceWidgetFactory)
    realtionchoice = RelationChoice(
        title=_(u'Related Choice'),
        source=ReferenceObjSourceBinder(),
        default=None,
        required=False,
    )

alsoProvides(IRelationChoiceExample, IFormFieldProvider)


class IDataGridRow(model.Schema):
    label = schema.TextLine(
        title=u'Label',
        default=u'I am the default label',
    )

    directives.widget(link=ReferenceWidgetFactory)
    link = RelationChoice(
        title=u'Link',
        source=ReferenceObjSourceBinder(),
        required=False,
    )


class IDataGridFieldExample(Interface):
    """Demo behavior containing a DataGridField.

    """
    directives.widget('the_data_grid', DataGridFieldFactory, allow_reorder=True)
    the_data_grid = schema.List(
        title=u'The Data Grid',
        value_type=DictRow(title=u'the_data_grid_row', schema=IDataGridRow),
        required=False,
        missing_value=[],
    )


alsoProvides(IDataGridFieldExample, IFormFieldProvider)


class CustomSelectableClass(DefaultSelectable):

    def is_selectable(self):
        return self.content.Title() == 'Immutable title'


class IRelationChoiceRestricted(Interface):
    """Demo behavior containing a RelationChoice (single value).
    But it's not allowd to reference a folder.

    """
    directives.widget(realtionchoice_restricted=ReferenceWidgetFactory)
    realtionchoice_restricted = RelationChoice(
        title=_(u'Related Choice Restricted'),
        source=ReferenceObjSourceBinder(
            nonselectable=['Folder']),
        default=None,
        required=False,
    )

    directives.widget(realtionchoice_restricted_title=ReferenceWidgetFactory)
    realtionchoice_restricted_title = RelationChoice(
        title=_(u'Related Choice Restricted Title'),
        source=ReferenceObjSourceBinder(
            selectable_class=CustomSelectableClass),
        default=None,
        required=False,
    )

    directives.widget(realtionchoice_restricted_path=ReferenceWidgetFactory)
    realtionchoice_restricted_path = RelationChoice(
        title=_(u'Related Choice Restricted Title'),
        source=ReferenceObjSourceBinder(
            root_path='/testfolder'),
        default=None,
        required=False,
    )


alsoProvides(IRelationChoiceRestricted, IFormFieldProvider)
