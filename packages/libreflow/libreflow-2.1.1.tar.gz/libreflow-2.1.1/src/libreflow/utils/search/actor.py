import pymongo
import re

from kabaret.app._actor import Actor, Cmd, Cmds


#------ CMDS


class SearchCmds(Cmds):
    '''
    '''


@SearchCmds.cmd
class Query_Index(Cmd):
    '''
    Returns a list of dicts describing the first `limit` entries
    of the search index matching the given `query_filter`.

    The dict keys are the following:
        id       : unique id of the entry
        goto_oid : id of the flow object corresponding to this entry
        label    : entry label
    '''
    def _decode(self, query_filter=None, limit=10):
        self._query_filter = query_filter
        self._limit = limit

    def _execute(self):
        results = self.actor().query_index(
            self._query_filter,
            self._limit
        )
        return [r.to_dict() for r in results]


@SearchCmds.cmd
class Query_Project_Index(Cmd):
    '''
    Returns a list of dicts describing the first `limit` entries
    of the search index matching the given `query_filter` and
    referencing objects under the project `project_name`.

    The dict keys are similar to that returned by the Query_Index
    command.
    '''
    def _decode(self, project_name, query_filter=None, limit=10):
        self._project_name = project_name
        self._query_filter = query_filter
        self._limit = limit

    def _execute(self):
        results = self.actor().query_project_index(
            self._project_name,
            self._query_filter,
            self._limit
        )
        return [r.to_dict() for r in results]


@SearchCmds.cmd
class List_Project_Names(Cmd):
    '''
    Returns a list containing the names of all projects
    existing on the cluster.
    '''
    def _decode(self):
        pass

    def _execute(self):
        return self.actor().get_project_names()


#------ Actor


class SearchResult:

    def __init__(self, actor, document):
        self._actor = actor
        self._document = None
        
        self.set_document(document)
    
    def set_document(self, doc):
        self._document = doc
        self._document['id'] = self._document.pop('_id')
    
    def id(self):
        return str(self._document['id'])
    
    def goto_oid(self):
        return self._document['goto_oid']
    
    def label(self):
        return self._document['label']
    
    def to_dict(self):
        return self._document


class Search(Actor):
    '''
    The Search actor manages a single search index for all projects
    defined in the cluster.
    Search entries are indexed in the `Search:index` collection
    within the <CLUSTER_NAME> Mongo database.
    '''

    def __init__(self, session, mongo_uri):
        super(Search, self).__init__(session)
        
        self._mongo_uri = mongo_uri
        self._mongo_client = None
    
    def _create_cmds(self):
        return SearchCmds(self)
    
    def on_session_connected(self):
        self.log('Configuring Search Engine')
        cluster = self.session().get_actor('Cluster')
        cluster_name = cluster.get_cluster_name()
        
        self._mongo_client = pymongo.MongoClient(
            self._mongo_uri,
            appname=self.session().session_uid()
        )
        self._index_collection = self._mongo_client[cluster_name]['Search:index']
    
    def get_result(self, document):
        return SearchResult(self, document)
    
    def query_index(self, query_filter=None, limit=10):
        '''
        Returns the `limit` indexed search entries with the highest
        similarity score with the given filter, ordered by score.
        '''
        # TODO filter using a computed score
        if query_filter is None:
            query_filter = {}
        else:
            tokens = query_filter.split()
            query_filter = {'goto_oid': {'$regex': '.*'.join(tokens)}}
        
        results = [
            self.get_result(doc)
            for doc in self._index_collection.find(query_filter, limit=limit)
        ]
        return results
    
    def get_project_names(self):
        return [
            project_name for project_name, _ in self.session().get_actor('Flow').get_projects_info()
        ]
    
    def query_project_index(self, project_name, query_filter=None, limit=10):
        if query_filter is not None:
            query_filter = f'^/{project_name} {query_filter}'
        
        return self.query_index(query_filter, limit)
    
    def build_project_indexes(self, oid_seed_list=None):
        self._index_collection.delete_many({})
        self.crawl_projects(oid_seed_list)
    
    def crawl_projects(self, oid_seed_list=None):
        '''
        oid_seed_list: list of tuples (oid seed, regex filter)
        '''
        for project_name, _ in self.session().get_actor('Flow').get_projects_info():
            self.crawl_project(project_name, oid_seed_list)
    
    def crawl_project(self, project_name, oid_seed_list=None):
        if oid_seed_list is None:
            # Check if project provides a list of oid seeds
            try:
                oid_seed_list = self.session().cmds.Flow.call(
                    '/'+project_name, 'get_search_oid_seeds', {}, {}
                )
            except AttributeError:
                self.session().log_warning((
                    f'Project {project_name} has not been crawled '
                    'since no oid seed has been provided.'
                ))
                return

        for from_oid, filter, depth in oid_seed_list:
            for oid in self.glob_project(project_name, from_oid, filter, depth):
                self._create_entry(oid)
    
    def glob_project(self, project_name, from_oid, oid_filter, depth):
        if not from_oid.startswith('/'+project_name):
            # Object identified by from_oid doesn't belong to the project
            return []
        
        return self._glob(from_oid, from_oid+'/'+oid_filter, 0, depth)
            
    def _glob(self, from_oid, oid_filter, depth, max_depth=1):
        matches = []

        if re.match(oid_filter, from_oid) is not None:
            matches.append(from_oid)
        
        if depth == max_depth:
            return matches

        for oid in self._ls(from_oid):
            if oid.startswith(from_oid):
                matches += self._glob(oid, oid_filter, depth + 1, max_depth)
        
        return matches
    
    def _ls(self, oid):
        from_relations = self.session().cmds.Flow.ls(oid)
        
        child_oids  = [child_oid for child_oid, _, _, _, _, _ in from_relations[0]]
        child_oids += [oid+'/'+mapped_name for mapped_name in from_relations[1]]
        
        return child_oids
    
    def _create_entry(self, oid):
        self._index_collection.insert_one({
            'goto_oid': oid,
            'label': self.session().cmds.Flow.get_source_display(oid)
        })