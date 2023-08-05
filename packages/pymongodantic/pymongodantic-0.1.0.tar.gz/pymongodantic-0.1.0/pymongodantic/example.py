from pymongodantic.collection import Collection
from pymongo import MongoClient

client = MongoClient('mongodb+srv://LINK')
db = client.get_database('pymongodantictesting')
nicecollection = db.get_collection('nicecollection')


class TestModel(Collection):
    _collection = nicecollection
    id: int
    test_name: str


if __name__ == '__main__':
    test1 = TestModel(id=1, test_name='wowdude')
    test2 = TestModel(id=2, test_name='wowdudeeee')
    test1.insert_self()
    TestModel.insert_one(test2)
    TestModel.insert_many([test1, test2])
    print(TestModel.find_one({'test_name': 'wowdude'}))
    # Supports all the same methods as pymongo.collection.Collection