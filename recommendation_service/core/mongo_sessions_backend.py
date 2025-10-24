from django.conf import settings
from django.contrib.sessions.backends.base import SessionBase, CreateError

from pymongo import MongoClient
from datetime import datetime, timedelta


_client = MongoClient(settings.DATABASE_URL)  # один раз на процес
_db = _client.get_database()  # автоматично бере назву з URI
_collection = _db["sessions"]

class SessionStore(SessionBase):
    def __init__(self, session_key=None):
        super().__init__(session_key)
        self.collection = _collection

    def load(self):
        session = self.collection.find_one({"session_key": self.session_key})
        if session and session.get("expire_date", datetime.now())> datetime.now():
            return self.decode(session["session_data"])
        self._session_key = self._get_new_session_key()
        return {}
    
    def create(self, must_create=False):
        session_data = self.encode(self._get_session(no_load=must_create))  
        data = {
            "session_key": self.session_key,
            "session_data": session_data,
            "expire_date": datetime.now() + timedelta(days=30),
        }

        if must_create:
            if self.collection.find_one({"session_key": self.session_key}):
                raise CreateError
            self.collection.insert_one(data)
        else:
            self.collection.update_one({"session_key": self.session_key}, {"$set": data}, upsert=True)

    def save(self, must_create=False):
        session_data = self.encode(self._get_session(no_load=must_create))  
        data = {
            "session_key": self.session_key,
            "session_data": session_data,
            "expire_date": datetime.now() + timedelta(days=30),
        }
        if must_create:
            if self.collection.find_one({"session_key": self.session_key}):
                raise CreateError
            self.collection.insert_one(data)
        else:
            self.collection.update_one({"session_key": self.session_key}, {"$set": data}, upsert=True)

    def exists(self, session_key):
        return self.collection.find_one({"session_key": session_key}) is not None
    
    def delete(self, session_key=None):
        self.collection.delete_one({"session_key": session_key or self.session_key})