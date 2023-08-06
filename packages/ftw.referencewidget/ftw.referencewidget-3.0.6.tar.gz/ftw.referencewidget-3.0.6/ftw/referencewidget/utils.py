from ftw.referencewidget import IS_PLONE_5_OR_GREATER
from plone import api
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility


def get_types_not_searched(context):

    if IS_PLONE_5_OR_GREATER:
        return api.portal.get_registry_record('plone.types_not_searched')
    else:
        portal_props = getToolByName(context, 'portal_properties')
        return portal_props.site_properties.types_not_searched


def set_types_not_searched(context, types):

    if IS_PLONE_5_OR_GREATER:
        from Products.CMFPlone.interfaces import ISearchSchema

        registry = getUtility(IRegistry)
        search_settings = registry.forInterface(ISearchSchema, prefix='plone')
        search_settings.types_not_searched = tuple(types)

    else:
        portal_props = getToolByName(context, 'portal_properties')
        portal_props.site_properties.types_not_searched = types
