from datetime import datetime, date, time
from sqlalchemy import create_engine, event
from sqlalchemy.orm import scoped_session, sessionmaker, aliased, mapper
from sqlalchemy.dialects import mysql
from sqlalchemy import exists, desc, text, and_
from sqlalchemy.inspection import inspect
from scrapeanything.database.models import Model

from scrapeanything.utils.types import Types
from scrapeanything.utils.utils import Utils
from scrapeanything.utils.config import Config
from scrapeanything.utils.log import Log

class Repository:

    def __init__(self, config: Config) -> None:
        self.config = config

        is_debug = True if self.config.get(section='COMMANDS', key='debug') == 'True' else False

        username = self.config.get(section='DATABASE', key='username')
        password = self.config.get(section='DATABASE', key='password')
        host = self.config.get(section='DATABASE', key='host')
        port = self.config.get(section='DATABASE', key='port')
        database = self.config.get(section='DATABASE', key='database')
        self.engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}', echo=is_debug) # , isolation_level='READ UNCOMMITTED')
        Session = sessionmaker(bind=self.engine)
        self.session = scoped_session(Session)
  
    def save(self, entity: any) -> None:
        '''
        Description: save a collection of models or a single model
        Arguments: <data> - collection or single model
        Returns: last id inserted or updated
        '''
        response = None
        data = entity

        #region entity
        model_from_database = self.load(entity=data)
        model = self.update(entity_from_database=model_from_database, entity=data)

        if model not in self.session:
            self.session.merge(model)

        entity_type = type(model)
        Log.trace('Saved entity {0} with id {1}', entity_type, model.id)
        #endregion entity

    def update(self, entity_from_database: any, entity: any) -> any:
        '''
        Description: updates an entity from its version on the database
        Arguments: 
        - <entity_from_database> - entity loaded from the database
        - <entity> - entity built in memory
        Returns: updated entity (holds Id from the database saved entity)
        '''

        if entity_from_database is None:
            return entity

        mapper = inspect(entity)
        for attr in mapper.attrs:
            if attr.key == 'id' or attr.key == 'created_at' or attr.key == 'updated_at':
                continue
            # elif attr.key.endswith('s'):
            #     continue
            elif attr.key.endswith('id'):
                continue

            value = getattr(entity, attr.key)
            if Types.is_primitive(value=value) and getattr(entity_from_database, attr.key) != value:
                setattr(entity_from_database, attr.key, value)

        return entity_from_database

    def load(self, entity: any):
        '''
        Description:
        Arguments:
        Returns:
        '''

        entity_type = type(entity)
        filters = self.get_keys(entity=entity)
        from_database = self.first(entity_type, filters)
        return from_database

    def first(self, entity_type: any, filters: list):
        '''
        Description: returns the first element found given some filters
        Arguments:
        Returns:
        '''

        query = self.session.query(entity_type)

        aliases = {}
        for attr, value in filters.items():
            # condition is of type object.subobject.property = value
            if attr.find('.') > -1:

                entities = attr.split('.')[:-1] # from object.subobject1.subobject2.property take object.subobject1.subobject2
                attribute = attr.split('.')[-1] # from object.subobject1.subobject2.property last attribute is property

                parent_entity_type = entity_type
                for i, sub_entity in enumerate(entities): # from object.subobject1.subobject2.property get only object.subobject1.subobject2
                    # subobject<i>
                    sub_entity_type = Types.to_class(module_name='database.models', class_name=self.get_sub_entity_type(entity=parent_entity_type, prop=sub_entity))
                    aliases[sub_entity] = aliased(sub_entity_type)
                    # join
                    query = query.join(aliases[sub_entity], Utils.find(parent_entity_type, sub_entity))

                    # joins have to be executed on [object, subobject1]; [suboject1, suboject2]; etc.
                    parent_entity_type = sub_entity_type

                # filter
                # load an object by similarity
                if self.config.get(section='DATABASE', key='load_filter', default='equal') == 'like':
                    condition = getattr(aliases[sub_entity], attribute).like(f'%{value}%')
                else:
                    condition = getattr(aliases[sub_entity], attribute) == value

                query = query.filter(condition)

            # condition is of type object.property = value
            elif attr.find('.') == -1:
                if self.config.get(section='DATABASE', key='load_filter', default='equal') == 'like':
                    condition = getattr(entity_type, attr).like(f'%{value}%')
                else:
                    condition = getattr(entity_type, attr) == value

                # add condition to the query 
                query = query.filter(condition)

        entity = query.first()
        return entity

    def all(self, entity_type):
        '''
        Description:
        Arguments:
        Returns:
        '''

        entity_type = Types.to_class(module_name='database.models', class_name=entity_type)
        entities = self.session.query(entity_type).all()
        return entities

    def get_keys(self, entity: any):
        '''
        Description: Returns list of columns and their values to determine uniquely a given entity (defined in models.py)
        Arguments:
        Returns:
        '''

        def normalize_keys(keys: list):
            normalized_keys = []

            for key in keys:
                if key.find('*') > -1:
                    entity = key.split('.')[-2] # take the last entity before *
                    entity_type = entity.split('_')[0].capitalize()
                    entity_type = Types.to_class(module_name='database.models', class_name=entity_type)

                    for token in entity_type.__keys__.split(','):
                        token = token.strip()
                        normalized_key = key.replace('*', token)
                        normalized_keys += normalize_keys([ normalized_key ])
                else:
                    normalized_keys.append(key)

            return normalized_keys

        def replace_star_in_key(keys: str):
            # supports __keys__ = match.*

            response = []

            for key in keys.split(','):
                key = key.strip()
                if key.find('*') > -1:
                    ref_entity = key.strip().split('.')[-2] # another_entity
                    ref_entity_type = ref_entity.split('_')[0].capitalize().strip() if ref_entity.find('_') != -1 else ref_entity.capitalize().strip() # extract entity name # TODO: use self.get_sub_entity_type()?
                    ref_entity_type = Types.to_class(module_name='database.models', class_name=ref_entity_type.capitalize().strip())
                    exploded_keys = ref_entity_type.__keys__ # __keys__ of another_entity

                    # exploded_keys are taken from child entity (i.e. match.* => championship.name, team_home.name, team_away.name).
                    # Prepende at each reference property the source object (i.e. match.championship.name, match.team_home.name, match.team_away.name)
                    for exploded_key in exploded_keys.split(','):
                        exploded_key = exploded_key.strip()
                        if exploded_key.find('*') > -1:
                            exploded_key = f'{ref_entity}.{exploded_key.strip()}'
                            response.append(replace_star_in_key(keys=exploded_key))
                        else:
                            response.append(f'{ref_entity}.{exploded_key.strip()}')
                else:
                    response.append(key)

            return response
        
        filters = {}

        # for <entity> there could be some columns that refer to __keys__ of another entity (i.e. other_entity.another_entity.*)
        __keys__ = normalize_keys(keys=[ key.strip() for key in entity.__keys__.split(',') ])

        # get all keys listed comma separated
        for key in __keys__:
            filters[key] = eval(f'entity.{key}') # Utils.find(entity, key) # { key: value }

        return filters

    def get_raw_query(self, q: any):
        '''
        Description: transforms SqlAlchemy query into t-sql query (It can be used for debugging purposes)
        Arguments: <q> - SqlAlchemy query (from self.session(<q>))
        Returns: t-sql query string version
        '''

        query = q.statement.compile(dialect=mysql.dialect())
        params = query.params # get query parameters and values

        query_string = str(q.as_scalar()) # get query in t-sql format. It contains constants as query parameters (i.e. SELECT * FROM table WHERE value = :value)
        for param, value in params.items():

             # replace query parameters with real values
            if type(value) is str:
                value = f"'{value}'"
            elif type(value) is date:
                value = f"'{datetime.strftime(value, '%Y-%M-%d')}'"
            elif type(value) is time:
                value = f"'{datetime.strftime(value, '%H-%m-%s')}'"
            elif type(value) is datetime:
                value = f"'{datetime.strftime(value, '%Y-%M-%d %H-%m-%s')}'"

            query_string = query_string.replace(f':{param}', str(value))

        query_string = query_string.replace('\n', '') # the query contains some "\n". Let's remove them
        query_string = query_string[1:-1] # remove initial "(" and last ")" form query_string

        return query_string

    def get_sub_entity_type(self, entity: any, prop: str):
        '''
        Description: <TODO>
        Arguments: <TODO>
        Returns: <TODO>
        '''

        try:
            return getattr(entity, prop).property.argument
        except:
            key = getattr(entity, prop).property.key
            if key == 'team_home' or 'team_away':
                return 'Team'
            if key == 'match':
                return 'Match'
            if key == 'bet':
                return 'Bet'

    def query(self, entity_type):
        return self.session.query(entity_type)

    def sql(self, query: str, parameters: dict=None, entity_type: any=None) -> any:
        '''
        Executes sql query. Make sure you use :parameter for parameters
        '''
        q = text(query)
        result = self.engine.execute(q, parameters).fetchall()
        return result

    def assign(self, entity, prop, value):
        loaded_value = self.load(entity=value)
        value = self.update(entity_from_database=loaded_value, entity=value)
        if type(value) is list:
            for v in value:
                if v not in self.session:
                    value.is_dirty = True
                setattr(entity, prop, value)
        else:
            if value not in self.session:
                value.is_dirty = True
            setattr(entity, prop, value)

        return entity

    def rollback(self):
        self.session.rollback()

    def commit(self):
        self.session.commit()

    def close(self):
        self.session.close()
        self.engine.dispose()