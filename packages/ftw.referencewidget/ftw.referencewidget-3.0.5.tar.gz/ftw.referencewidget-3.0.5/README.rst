ftw.referencewidget
===================

This Widget provides a Referencebrowser and a searchfield, which allows users to select references.

The basequery is all types which are not in the types_not_searched property all modification to the allowed types are relative to this query.

Traversal or Selectability can be changed for all widgets with the IReferenceSettings registry interface or per widget with the widget parameters.

The widget takes the following parameters:
 - allow_traversal: List of Types which are added as traversable. Will act as complete configuration if `override` is set to True.
 - block_traversal: List of Types which are added as not traversable. Will be ignored if `override` is set to True.
 - selectable: List of Types which are added to the as selectable. Will act as complete configuration if `override` is set to True
 - nonselectable: List of Types which are added as not selectable. Will be ignored if `override` is set to True.
 - start: The path first opened. Can either be a callable or a path. Additionaly the strings "parent", "navroot", "ploneroot" can be used.
 - allow_nonsearched_types: If this is set to true all the types will be traversable and selectable.
 - override: Drops all global config and the base query if a list is passed to the widget. If this is set to true, `selectable` & `allow_traversal` are not additive but act as the complete configuration instead. `nonselectable` & `block_traversal` will be ignored.
 - traversal_query: Updates the query used vor traversing by the given dict. The dict passed will be updated after everything is allready done. So make sure not to override sort_on/sort_order attributes.


Upgrading from 1.x to 2.x
-------------------------

There was no version number set for the ``ftw.referencewidget`` package. As a result of this upgradesteps wont be shown in ``../@@manage-upgrades`` from `ftw.upgrade <https://github.com/4teamwork/ftw.upgrade>`_.
So the first upgradesetp ``Upgrade ftw.referencewidget:default to 20181112105705: Fix registry field frontend edit`` must be installed via the ZMI under ``../portal_setup/manage_fullImport``. This sets the version for the package and so further upgrades can be installed via ``../@@manage-upgrades``.

ContextSourceBinder
-------------------

With a `RelationeChoice` or `RelationList` of `RelationChoice` a source can be configured along with the field.
The `ContextSourceBinder` makes sure that only valid content can be selected.

By default, the source binder only checks for a valid portal_type when selecting content.

The default_filter implementation therefore looks like this:

.. code:: python

    def default_filter(source, value):
        """"
        Return ``True`` when the object is selectable, ``False``
        when it is not selectable.

        """"
        return value.portal_type in get_selectable_types_by_source(source)

Feel free to add your own filter method as source parameter in your field.
Example:

.. code:: python

    from ftw.referencewidget.filter import DefaultSelectable

    class CustomClass(DefaultSelectable):
        def is_selectable(self):
            return bool(..)
    ...

    directives.widget(realtionchoice_restricted_title=ReferenceWidgetFactory)
    realtionchoice_restricted_title = RelationChoice(
        title=_(u'Related Choice Restricted Title'),
        source=ReferenceObjSourceBinder(
            selectable_class=CustomClass),
        default=None,
        required=False,
    )

The `filter` takes two parameter the actual source object and a value, which is the content object.

Only `ReferenceObjSourceBinder` are supported. The SourceBinder takes the following parameters:

- selectable: Adds these types as selectable. Will act as complete configuration if `override` is set to True
- nonselectable: Adds these Types are not selectable. Will be ignored if `override` is set to True.
- allow_nonsearched_types: If this is set to true all the types will be traversable and selectable.
- override: Drops all global config and the base query if a list is passed to the widget. If this is set to true, `selectable` is not additive but acts as the complete configuration instead. `nonselectable` will be ignored.
- selectable_class: Custom ISelectable Class to determine if a content is selectable or not.

The parameters are same as for the widget (Backwards compatibility with 1.x releases).


Fields combinations (Registered converter)
------------------------------------------

The following combinations are supported:

- RelationList with value_type Relation --> Stores a List of RelationValues
- RelationList with value_type RelationChoice --> Stores a List of RelationValues
- Relation --> Stores a RelationValue
- List of RelationChoice --> Stores a list of absolute paths, without the portal root part
- TextLine --> Stores a absolute path as string, without the portal root part


TinyMCE Plone 5 - Internal Link widget replacement
--------------------------------------------------

With the version 3 of ftw.referencewidget within Plone 5.x the select2 internal link widget
automatically gets replaced by the ftw.referencewidget interna link browser.
Featering search and browsing within the referencebrowser popup. 


Screenshots
-----------
The general Listing:
![Listing](https://github.com/4teamwork/ftw.referencewidget/raw/master/docs/static/list.png)
The Search Listing:
![Search Listing](https://github.com/4teamwork/ftw.referencewidget/raw/master/docs/static/search.png)
The Selected Items
![Selected](https://github.com/4teamwork/ftw.referencewidget/raw/master/docs/static/selected.png)

Links
-----

- Github: https://github.com/4teamwork/ftw.referencewidget
- Issues: https://github.com/4teamwork/ftw.referencewidget/issues
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.referencewidget


Copyright
---------

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.referencewidget`` is licensed under GNU General Public License, version 2.
