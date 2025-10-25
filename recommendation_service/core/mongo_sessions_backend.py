from django.conf import settings
from django.contrib.sessions.backends.base import SessionBase, CreateError

from pymongo import MongoClient
from datetime import datetime, timedelta


_client = MongoClient(settings.DATABASE_URL) 
_db = _client.get_database() 
collection = _db["sessions"]


class SessionStore(SessionBase):
    """Working with sessions associated with the user model MongoDB."""
    def __init__(self, session_key=None):
        super().__init__(session_key)
        self.collection = collection

    def load(self):
        session = self.collection.find_one({"session_key": self.session_key})
        if session and session.get("expire_date") > datetime.now():
            return self.decode(session["session_data"])
        return {}

    def create(self):
        self._session_key = self._get_new_session_key()
        self.save(must_create=True)

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
        return bool(self.collection.find_one({"session_key": session_key is not None}))
    
    def delete(self, session_key=None):
        self.collection.delete_one({"session_key": session_key or self.session_key})

    def create_or_save(self, session_key):
        if self.exists(session_key):
            return self.save()
        return self.create()