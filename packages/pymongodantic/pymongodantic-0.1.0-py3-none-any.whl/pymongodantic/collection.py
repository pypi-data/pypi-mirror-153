from pymongo.collection import Collection as MongoCollection
from pydantic import BaseModel

class Collection(BaseModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    _collection: MongoCollection

    @staticmethod
    def _test_and_apply_one(cb, doc, *args, **kwargs):
        if isinstance(doc, BaseModel):
            doc = doc.dict()
            return cb(doc, *args, **kwargs)
        elif type(doc) is dict:
            return cb(doc, *args, **kwargs)
        raise TypeError(f'{type(doc)} is not a dict or BaseModel')

    @staticmethod
    def _test_and_apply_many(cb, docs, *args, **kwargs):
        if isinstance(docs, list):
            if all(isinstance(x, dict) for x in docs):
                return cb(docs, *args, **kwargs)
            elif all(isinstance(x, BaseModel) for x in docs):
                return cb([x.dict() for x in docs], *args, **kwargs)
            raise TypeError(f'{type(docs)} is not a list with dicts or BaseModels')
        raise TypeError(f'{type(docs)} is not a list')

    def insert_self(self, bypass_document_validation=False,
                   session=None):
        return self._test_and_apply_one(self._collection.insert_one, self, bypass_document_validation, session)

    @classmethod
    def insert_one(cls, document, bypass_document_validation=False,
                   session=None):
        return cls._test_and_apply_one(cls._collection.insert_one, document, bypass_document_validation, session)

    @classmethod
    def insert_many(cls, documents, ordered=True,
                    bypass_document_validation=False, session=None):
        return cls._test_and_apply_many(cls._collection.insert_many, documents, ordered, bypass_document_validation, session)

    @classmethod
    def replace_one(cls, filter, replacement, upsert=False,
                    bypass_document_validation=False, collation=None,
                    hint=None, session=None):
        return cls._test_and_apply_one(cls._collection.replace_one, filter, replacement, upsert, bypass_document_validation, collation, hint, session)
    
    @classmethod
    def update_one(cls, filter, update, upsert=False,
                   bypass_document_validation=False, collation=None,
                   array_filters=None, session=None):
        return cls._test_and_apply_one(cls._collection.update_one, filter, update, upsert, bypass_document_validation, collation, array_filters, session)

    @classmethod
    def update_many(cls, filter, update, upsert=False,
                    bypass_document_validation=False, collation=None,
                    array_filters=None, session=None):
        return cls._test_and_apply_many(cls._collection.update_many, filter, update, upsert, bypass_document_validation, collation, array_filters, session)

    @classmethod
    def delete_one(cls, filter, collation=None, session=None):
        return cls._test_and_apply_one(cls._collection.delete_one, filter, collation, session)

    @classmethod
    def delete_many(cls, filter, collation=None, session=None):
        return cls._test_and_apply_many(cls._collection.delete_many, filter, collation, session)

    @classmethod
    def find(cls, filter=None, projection=None, skip=0, limit=0,
                no_cursor_timeout=False, cursor_type=0, sort=None,
                allow_partial_results=False, oplog_replay=False, modifiers=None):
            return [cls.parse_obj(x) for x in cls._test_and_apply_one(cls._collection.find, filter, projection, skip, limit, no_cursor_timeout, cursor_type, sort, allow_partial_results, oplog_replay, modifiers)]

    @classmethod
    def find_one(cls, filter=None, projection=None, skip=0,
                    no_cursor_timeout=False, oplog_replay=False,
                    modifiers=None, session=None,):
            return cls.parse_obj(cls._test_and_apply_one(cls._collection.find_one, filter, projection=projection, skip=skip, no_cursor_timeout=no_cursor_timeout, oplog_replay=oplog_replay, modifiers=modifiers, session=session))


    # TODO: Add support in pydantic for below
    @classmethod
    def aggregate(cls, pipeline, collation=None, session=None):
        return cls._collection.aggregate(pipeline, collation, session)

    @classmethod
    def count_documents(cls, filter, session=None):
        return cls._collection.count_documents(filter, session)

    @classmethod
    def distinct(cls, key, filter=None, session=None):
        return cls._collection.distinct(key, filter, session)

    @classmethod
    def group(cls, key, condition, initial, reduce, finalize=None, command=False,
                collation=None, session=None):
        return cls._collection.group(key, condition, initial, reduce, finalize, command, collation, session)

    @classmethod
    def map_reduce(cls, map, reduce, out, full_response=False,
                    limit=None, scope=None, sort=None,
                    query=None, session=None):
        return cls._collection.map_reduce(map, reduce, out, full_response, limit, scope, sort, query, session)

    @classmethod
    def inline_map_reduce(cls, map, reduce, full_response=False,
                            scope=None, session=None):
            return cls._collection.inline_map_reduce(map, reduce, full_response, scope, session)


    
