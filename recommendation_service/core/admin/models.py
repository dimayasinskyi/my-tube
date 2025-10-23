from mongoengine import Document, StringField, EmailField, BooleanField
from werkzeug.security import generate_password_hash, check_password_hash


class User(Document):
    """
    Basic user model Mongodb.

    Has fiedls:
    - username
    - email 
    - password_hash
    - is_staff
    - is_superuser
    - is_active

    Has methods:
    - set_passwrod returns None
    - check_password returns Bool
    """
    username = StringField(required=True, unique=True)
    email = EmailField()
    password_hash = StringField(required=True)
    is_staff = BooleanField(default=False)
    is_superuser = BooleanField(default=False)
    is_active = BooleanField(default=True)

    def set_password(self, password) -> None:
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)