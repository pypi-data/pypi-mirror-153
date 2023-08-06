from collective.z3cform.datagridfield.interfaces import IDataGridField
from ftw.referencewidget.interfaces import IReferenceWidget
from plone import api
from z3c.form import converter
from z3c.relationfield import RelationValue
from z3c.relationfield.event import _setRelation
from z3c.relationfield.interfaces import IRelation
from z3c.relationfield.interfaces import IRelationChoice
from z3c.relationfield.interfaces import IRelationList
from zope import component
from zope.component import adapts
from zope.intid.interfaces import IIntIds
from zope.schema.interfaces import IList
from zope.schema.interfaces import ITextLine
import os


class ReferenceDataListConverter(converter.BaseDataConverter):

    adapts(IRelationList, IReferenceWidget)

    def toFieldValue(self, value):
        if not value:
            return self.field.missing_value
        elif isinstance(value, unicode):
            return [self.widget.context.unrestrictedTraverse(
                value.encode("utf8"))]

        elif isinstance(value, basestring):
            return [self.widget.context.unrestrictedTraverse(value)]

        else:
            result = []
            for item in value:
                if not item:
                    continue
                result.append(self.widget.context.unrestrictedTraverse(
                    item.encode("utf-8")))
            return result

    def toWidgetValue(self, value):
        result = []
        for item in value:
            result.append('/'.join(item.getPhysicalPath()))
        return result


class ReferenceDataChoiceConverter(converter.BaseDataConverter):

    adapts(IRelation, IReferenceWidget)

    def toFieldValue(self, value):
        if not value:
            return self.field.missing_value
        elif isinstance(value, unicode):
            return self.widget.context.unrestrictedTraverse(
                value.encode("utf8"))

        elif isinstance(value, basestring):
            return self.widget.context.unrestrictedTraverse(value)

        else:
            return self.widget.context.unrestrictedTraverse(
                value[0].encode("utf-8"))

    def toWidgetValue(self, value):
        if value:
            return '/'.join(value.getPhysicalPath())


class ReferenceDataTextConverter(converter.BaseDataConverter):

    adapts(ITextLine, IReferenceWidget)

    def toFieldValue(self, value):
        if not value:
            return
        elif isinstance(value, list):
            # Since there is always a empty hidden field it's always a list :-(
            value, = [path for path in value if path]

        portal_path = '/'.join(api.portal.get().getPhysicalPath())
        return os.path.relpath(value, portal_path)

    def toWidgetValue(self, value):
        if value:

            # For Backwards compatibility with ContentTreeFieldWidget
            value = value.startswith('/') and value[1:] or value

            portal_path = '/'.join(api.portal.get().getPhysicalPath())
            return '/'.join([portal_path, value])
        else:
            return value


class ReferenceDataListWithChoiceConverter(converter.BaseDataConverter):
    """Converter of IList of IRelationChoices."""

    adapts(IList, IReferenceWidget)

    def toFieldValue(self, value):
        portal_path = '/'.join(api.portal.get().getPhysicalPath())

        if not value:
            return []
        elif isinstance(value, (unicode, str)):
            return [os.path.relpath(value, portal_path)]
        else:
            portal_path = '/'.join(api.portal.get().getPhysicalPath())
            return map(
                lambda path: os.path.relpath(path, portal_path),
                filter(lambda path: bool(path), value))

    def toWidgetValue(self, value):
        if value:
            portal_path = '/'.join(api.portal.get().getPhysicalPath())
            return map(lambda path: '/'.join([portal_path, path]), value)
        else:
            return value


class GridDataConverter(converter.BaseDataConverter):
    """
    The value of a RelationChoice schema field usually is stored as a relation value
    in the database but the data grid stores the item as-is (an object, not a relation).

    So we need to convert the object to a relation value before storing it in the database
    and convert it to an object when rendering the widget.

    Inspired by https://github.com/collective/collective.z3cform.datagridfield/issues/50.
    """
    adapts(IList, IDataGridField)

    def toWidgetValue(self, value):
        if not value:
            return value
        new_value = []
        for row in value:
            new_row = {}
            for key in row:
                new_row[key] = row[key]
                if row[key] and IRelationChoice.providedBy(self.field.value_type.schema[key]):
                    if hasattr(row[key], 'to_object'):
                        new_row[key] = row[key].to_object
            new_value.append(new_row)
        return new_value

    def toFieldValue(self, value):
        if not value:
            return value
        intids = component.queryUtility(IIntIds)
        for row in value:
            for key in row:
                if row[key] and IRelationChoice.providedBy(self.field.value_type.schema[key]):
                    to_id = intids.queryId(row[key])
                    if to_id:
                        relation = RelationValue(to_id)
                        _setRelation(row[key], key, relation)
                        row[key] = relation
        return value
