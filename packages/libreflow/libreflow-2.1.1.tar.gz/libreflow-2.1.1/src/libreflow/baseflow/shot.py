from kabaret import flow
from kabaret.flow_entities.entities import Entity, Property

from .maputils import SimpleCreateAction
from ..utils.kabaret.flow_entities.entities import EntityView


class Shot(Entity):
    """
    Defines a shot.

    Instances provide the `shot` key in their contextual
    dictionary (`settings` context).
    """

    ICON = ('icons.flow', 'shot')

    @classmethod
    def get_source_display(cls, oid):
        split = oid.split('/')
        return f'{split[3]} · {split[5]} · {split[7]}'

    def get_default_contextual_edits(self, context_name):
        if context_name == 'settings':
            return dict(shot=self.name())


class ShotCollection(EntityView):
    """
    Defines a collection of shots.
    """

    ICON = ('icons.flow', 'shot')

    add_shot = flow.Child(SimpleCreateAction)
    
    @classmethod
    def mapped_type(cls):
        return flow.injection.injectable(Shot)
    
    def collection_name(self):
        mgr = self.root().project().get_entity_manager()
        return mgr.get_shot_collection().collection_name()


class Sequence(Entity):
    """
    Defines a sequence containing a list of shots.

    Instances provide the `sequence` key in their contextual
    dictionary (`settings` context).
    """

    ICON = ('icons.flow', 'sequence')

    shots = flow.Child(ShotCollection).ui(
        expanded=True, 
        show_filter=True
    )

    @classmethod
    def get_source_display(cls, oid):
        split = oid.split('/')
        return f'{split[3]} · {split[5]}'

    def get_default_contextual_edits(self, context_name):
        if context_name == 'settings':
            return dict(sequence=self.name())


class SequenceCollection(EntityView):
    """
    Defines a collection of sequences.
    """

    ICON = ('icons.flow', 'sequence')
    
    add_sequence = flow.Child(SimpleCreateAction)
    
    @classmethod
    def mapped_type(cls):
        return flow.injection.injectable(Sequence)
    
    def collection_name(self):
        mgr = self.root().project().get_entity_manager()
        return mgr.get_sequence_collection().collection_name()
