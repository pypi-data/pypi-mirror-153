from kabaret import flow
from kabaret.flow_entities.store import EntityStore

from ..utils.kabaret.flow_entities.entities import GlobalEntityCollection


class EntityManager(flow.Object):
    '''
    This class manages the entity store of the project. It
    should contain the relations to the global entity collections
    of the project, and explicitly provide them redefining its
    getters.
    '''

    store = flow.Child(EntityStore)

    def get_film_collection(self):
        raise NotImplementedError((
            'Must return the collection containing all the '
            'films of this project.'
        ))

    def get_sequence_collection(self):
        raise NotImplementedError((
            'Must return the collection containing all the '
            'sequences of this project.'
        ))
    
    def get_shot_collection(self):
        raise NotImplementedError((
            'Must return the collection containing all the '
            'shots of this project.'
        ))
    
    def get_task_collection(self):
        raise NotImplementedError((
            'Must return the collection containing all the '
            'tasks of this project.'
        ))
    
    def get_file_collection(self):
        raise NotImplementedError((
            'Must return the collection containing all the '
            'files of this project.'
        ))
    
    def get_revision_collection(self):
        raise NotImplementedError((
            'Must return the collection containing all the '
            'revisions of this project.'
        ))
    
    def get_sync_status_collection(self):
        raise NotImplementedError((
            'Must return the collection containing all the '
            'synchronisation statutes of this project.'
        ))

    def get_action_value_collection(self):
        raise NotImplementedError((
            'Must return the collection containing all the '
            'synchronisation statutes of this project.'
        ))
