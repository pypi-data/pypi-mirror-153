import uuid
import time
from kabaret import flow
from kabaret.flow_entities.entities import Entity, EntityCollection, Property


class ActionValue(Entity):
    '''
    '''

    action_name = Property()
    site_name   = Property()
    key         = Property()
    value       = Property()
    is_default  = Property().ui(editor='bool')


class ActionValueStoreView(EntityCollection):
    '''
    This class defines a view on the project's action
    value store. One may subclass it to redefine at
    least the `query_filter()` method to filter store
    values.
    '''
    
    def collection_name(self):
        return self.root().project().get_action_value_store().collection_name()

    def collection(self):
        return self.get_entity_store().get_collection(
            self.collection_name()
        )


class EditSiteActionValue(flow.Action):

    value = flow.SessionParam('')

    _value_item  = flow.Parent()
    _values      = flow.Parent(2)
    _action_item = flow.Parent(3)
    _site        = flow.Parent(5)

    def get_buttons(self):
        current = self.root().project().get_action_value_store().get_action_value(
            self._action_item.name(),
            self._value_item.name(),
            self._site.name(),
        )
        self.value.set(current or '')
        return ['Save', 'Restore default']
    
    def run(self, button):
        store = self.root().project().get_action_value_store()

        if button == 'Save':
            store.update_site_override(
                self._action_item.name(),
                self._site.name(),
                self._value_item.name(),
                self.value.get(),
            )
        else:
            store.remove_override(
                self._action_item.name(),
                self._site.name(),
                self._value_item.name(),
            )

        self._values.touch()


class EditGenericActionValue(flow.Action):

    value = flow.SessionParam('')

    _value_item  = flow.Parent()
    _values      = flow.Parent(2)
    _action_item = flow.Parent(3)

    def get_buttons(self):
        current = self.root().project().get_action_value_store().get_action_value(
            self._action_item.name(),
            self.get_key(self._value_item.name()),
        )
        self.value.set(current or '')
        return ['Save', 'Restore default']
    
    def get_key(self, mapped_name):
        return self._values.get_key(mapped_name)
    
    def run(self, button):
        store = self.root().project().get_action_value_store()

        if button == 'Save':
            store.update_generic_value(
                self._action_item.name(),
                self.get_key(self._value_item.name()),
                self.value.get(),
                False
            )
        else:
            store.restore_default_value(
                self._action_item.name(),
                self.get_key(self._value_item.name()),
            )

        self._values.touch()


class GenericActionValueViewItem(Entity):

    edit = flow.Child(EditGenericActionValue)


class SiteActionValueViewItem(Entity):

    edit = flow.Child(EditSiteActionValue)


class GenericActionValueView(ActionValueStoreView):

    _item = flow.Parent()

    @classmethod
    def mapped_type(cls):
        return GenericActionValueViewItem

    def query_filter(self):
        return {
            '$and': [
                {'action_name': self._item.name()},
                {'site_name': None},
            ]
        }
    
    def columns(self):
        return ['Key', 'Value']
    
    def get_key(self, mapped_name):
        self.mapped_names()
        return self._document_cache[mapped_name]['key']
    
    def _fill_row_cells(self, row, item):
        self.mapped_names()
        item_data = self._document_cache[item.name()]
        row['Key'] = item_data['key']
        row['Value'] = item_data['value']
    
    def _fill_row_style(self, style, item, row):
        if self._document_cache[item.name()]['is_default']:
            for col in self.columns():
                style[col+'_foreground-color'] = '#606060'
        
        style['activate_oid'] = item.edit.oid()


class SiteActionValueView(GenericActionValueView):

    _site = flow.Parent(3)

    @classmethod
    def mapped_type(cls):
        return SiteActionValueViewItem

    def mapped_names(self, page_num=0, page_size=None):
        cache_key = (page_num, page_size)
        if (
            self._document_cache is None
            or self._document_cache_key != cache_key
            or self._document_cache_birth < time.time() - self._document_cache_ttl
        ):
            cursor = (
                self.get_entity_store()
                .get_collection(self.collection_name())
                .aggregate([
                    {
                        '$match': self.query_filter()
                    },
                    {
                        '$group': {'_id': '$key', 'values': {'$push': '$$ROOT'}},
                    }
                ])
            )
            if page_num is not None and page_size is not None:
                cursor.skip((page_num - 1) * page_size)
                cursor.limit(page_size)
            name_and_doc = [(i['_id'], i) for i in cursor]
            self._document_names_cache = [n for n, d in name_and_doc]
            self._document_cache = dict(name_and_doc)
            self._document_cache_birth = time.time()
            self._document_cache_key = cache_key
            self.ensure_indexes()

        return self._document_names_cache

    def query_filter(self):
        return {
            '$and': [
                {'action_name': self._item.name()},
                {
                    '$or': [
                        {'site_name': self._site.name()},
                        {'site_name': None},
                    ]
                }
            ]
        }
    
    def _fill_row_cells(self, row, item):
        self.mapped_names()
        
        key = item.name()
        value = None

        for v in self._document_cache[item.name()]['values']:
            value = v['value']
            if v['site_name'] == self._site.name():
                break
        
        row['Key'] = key
        row['Value'] = value
    
    def _fill_row_style(self, style, item, row):
        def paint_row(color):
            for col in self.columns():
                style[col+'_foreground-color'] = color
        
        for v in self._document_cache[item.name()]['values']:
            value = v
            if v['site_name'] == self._site.name():
                paint_row('#6ba1d3')
                break
        
        if v['is_default']:
            paint_row('#606060')
        
        style['activate_oid'] = item.edit.oid()


class GenericActionViewItem(Entity):
    
    values = flow.Child(GenericActionValueView)


class SiteActionViewItem(Entity):
    
    values = flow.Child(SiteActionValueView)


class ActionView(ActionValueStoreView):

    def mapped_names(self, page_num=0, page_size=None):
        cache_key = (page_num, page_size)
        if (
            self._document_cache is None
            or self._document_cache_key != cache_key
            or self._document_cache_birth < time.time() - self._document_cache_ttl
        ):
            cursor = (
                self.get_entity_store()
                .get_collection(self.collection_name())
                .aggregate([
                    {
                        '$match': self.query_filter()
                    },
                    {
                        '$group': {'_id': '$action_name', 'action_values': {'$push': '$$ROOT'}},
                    }
                ])
            )
            if page_num is not None and page_size is not None:
                cursor.skip((page_num - 1) * page_size)
                cursor.limit(page_size)
            name_and_doc = [(i['_id'], i) for i in cursor]
            self._document_names_cache = [n for n, d in name_and_doc]
            self._document_cache = dict(name_and_doc)
            self._document_cache_birth = time.time()
            self._document_cache_key = cache_key
            self.ensure_indexes()

        return self._document_names_cache

    def columns(self):
        return ['Action']
    
    def get_value(self, action_name, key):
        self.mapped_names()
        values = [
            v for v in self._document_cache[action_name]['action_values']
            if v['key'] == key
        ]
        # for v in values

    
    def _fill_row_cells(self, row, item):
        self.mapped_names()
        row['Action'] = item.name()


class GenericActionView(ActionView):

    @classmethod
    def mapped_type(cls):
        return GenericActionViewItem

    def query_filter(self):
        return {'site_name': None}


class SiteActionView(ActionView):

    _site = flow.Parent()

    @classmethod
    def mapped_type(cls):
        return SiteActionViewItem

    def query_filter(self):
        return {
            '$or': [
                {'site_name': self._site.name()},
                {'site_name': None},
            ]
        }


class ActionValueStore(EntityCollection):
    '''
    '''

    @classmethod
    def mapped_type(cls):
        return ActionValue
    
    def collection(self):
        return self.get_entity_store().get_collection(
            self.collection_name()
        )
    
    def get_action_values(self, action_name, default_values, use_site_overrides=True, site_name=None):
        '''
        Returns a dict containing the values provided
        in `default_values`, possibly overriden, in order
        of priority, by the values contained in:

          - the current site's override map
          - the project's action generic value map
        '''
        result_dict = default_values
        generic_values = self.get_generic_values(action_name)

        for v in generic_values:
            key = v['key']
            value = v['value']
            
            if v['is_default']:
                if default_values[key] != value:
                    # Action default value has changed: update generic default value
                    self.update_generic_value(action_name, key, default_values[key])
            else:
                # Generic override: update result value
                result_dict[key] = value
        
        # Inject action's new default values to project generic values
        new_values = {
            key: default for key, default in default_values.items()
            if key not in [generic['key'] for generic in generic_values]
        }
        self.ensure_default_values(action_name, new_values)

        if use_site_overrides:
            if site_name is None:
                site_name = self.root().project().get_current_site().name()
            
            # Override generic values with site's values
            site_values = self.get_site_overrides(action_name, site_name)
            
            for v in site_values:
                result_dict[v['key']] = v['value']
        
        return result_dict
    
    def ensure_default_values(self, action_name, default_values):
        '''
        Ensures values provided in the dict `default_values`
        exist in this collection.
        '''
        c = self.collection()
        new_values = []

        for key, value in default_values.items():
            if not c.find_one({
                'action_name': action_name,
                'site_name': None,
                'key': key,
            }):
                new_values.append((key, value))

        if not new_values:
            return
        
        c.insert_many([
            {
                'name': 'v'+uuid.uuid4().hex,
                'action_name': action_name,
                'site_name': None,
                'key': key,
                'value': value,
                'is_default': True,
            }
            for key, value in new_values
        ])
    
    def get_generic_values(self, action_name):
        return self.collection().find({
            'action_name': action_name,
            'site_name': None,
        })

    def update_generic_value(self, action_name, key, value, is_default=True):
        self.collection().update_one(
            {
                'action_name': action_name,
                'site_name': None,
                'key': key,
            },
            {
                '$set': {
                    'value': value,
                    'is_default': is_default
                }
            }
        )
    
    def restore_default_value(self, action_name, key):
        self.collection().update_one(
            {
                'action_name': action_name,
                'site_name': None,
                'key': key,
            },
            {
                '$set': {
                    'value': 'Default value to be restored at next action run',
                    'is_default': True
                }
            }
        )
    
    def update_site_override(self, action_name, site_name, key, value):
        doc = {
            'action_name': action_name,
            'site_name': site_name,
            'key': key,
        }
        c = self.collection()

        if not c.find_one(doc):
            doc.update({
                'name': 'v'+uuid.uuid4().hex,
                'value': value,
                'is_default': False,
            })
            c.insert_one(doc)
        else:
            c.update_one(
                doc,
                {
                    '$set': {
                        'value': value,
                        'is_default': False
                    }
                }
            )
    
    def get_action_value(self, action_name, key, site_name=None):
        value = None
        doc = self.collection().find_one({
            'action_name': action_name,
            'site_name': site_name,
            'key': key
        })

        if doc is not None:
            value = doc['value']
        
        return value
    
    def remove_override(self, action_name, site_name, key):
        self.collection().delete_one({
            'action_name': action_name,
            'site_name': site_name,
            'key': key,
        })

    def get_site_overrides(self, action_name, site_name):
        return self.collection().find({
            'action_name': action_name,
            'site_name': site_name,
        })

    def clear(self):
        self.collection().delete_many({})
