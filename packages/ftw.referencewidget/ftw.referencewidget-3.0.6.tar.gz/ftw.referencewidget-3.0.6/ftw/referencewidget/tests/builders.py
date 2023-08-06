from ftw.builder import registry
from ftw.builder.dexterity import DexterityBuilder
from ftw.referencewidget import IS_PLONE_5_OR_GREATER


class SampleContentBuilder(DexterityBuilder):
    portal_type = 'SampleContent'


registry.builder_registry.register(
    'refwidget sample content', SampleContentBuilder)


if IS_PLONE_5_OR_GREATER:

    class EventsBuilder(DexterityBuilder):
        portal_type = 'Event'

else:
    from ftw.builder.archetypes import ArchetypesBuilder

    class EventsBuilder(ArchetypesBuilder):
        portal_type = 'Event'


registry.builder_registry.register('event', EventsBuilder)
