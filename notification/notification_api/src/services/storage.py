from typing import Any

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import ServerSelectionTimeoutError

from src.utils.abstract import BaseStorage


class MongoStorage(BaseStorage):
    def __init__(self, client: MongoClient):
        self.client = client

    def connect(self, db_name: str, collection_name: str) -> Collection:
        db = self.client[db_name]
        collection = db[collection_name]
        return collection

    def get(self, collection: Collection, condition: dict) -> Any:
        try:
            doc = collection.find(condition)
        except ServerSelectionTimeoutError as error:
            print(type(error).__name__)
            return False
        return doc

    def insert(self, collection: Collection, data: dict) -> bool:
        try:
            collection.insert_one(data)
        except ServerSelectionTimeoutError as error:
            print(type(error).__name__)
            return False
        return True

    def update(self, collection: Collection, condition: dict, new_data: dict):
        try:
            doc = collection.find_one(condition)
            if doc:
                collection.update_one(doc, {'$set': new_data})
        except ServerSelectionTimeoutError as error:
            print(type(error).__name__)
            return False
        return True

    def delete(self, collection: Collection, condition: dict):
        try:
            doc = collection.find_one(condition)
            if doc:
                collection.delete_one(doc)
        except ServerSelectionTimeoutError as error:
            print(type(error).__name__)
            return False
        return True