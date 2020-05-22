import pymongo
import time


class Database:
    __instance = None
    __connectionString = "mongodb+srv://watchdog:example@clef-uaic-svoxc.mongodb.net/test?retryWrites=true&w=majority"

    def __init__(self):
        if Database.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Database.__instance = self
            client = pymongo.MongoClient(self.__connectionString)
            self.db = client['Tweets']

    @staticmethod
    def get_instance():
        if Database.__instance == None:
            Database()
        return Database.__instance


def get_current_time():
    return int(time.time())


def update_document_time_final(document_field, updated_time):
    db = Database.get_instance().db
    collection = db['experiments']

    doc_cursor = collection.find().sort('experiment_id', -1).limit(1)
    experiment_doc = None
    for doc in doc_cursor:
        experiment_doc = doc

    collection.update_one({'_id': experiment_doc['_id']}, {'$set': {
        document_field: updated_time
    }})

    return updated_time


def update_document_time(document_field):
    current_time = get_current_time()
    return update_document_time_final(document_field, current_time)


def update_start_time(module_name):
    document_field = 'module_' + module_name + '_start'
    return update_document_time(document_field)


def update_end_time(module_name):
    document_field = 'module_' + module_name + '_end'
    return update_document_time(document_field)


def update_end_time_duration(module_name, end_time):
    document_field = 'module_' + module_name + '_end'
    update_document_time_final(document_field, end_time)
