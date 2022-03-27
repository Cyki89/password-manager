from backend import db_manager


class classproperty(object):
    def __init__(self, func):
        self.func = func
    
    def __get__(self, obj, owner):
        return self.func(owner)


class User:
    logged_user = None

    def __init__(self, user_data): 
        self._id = user_data['_id']      
        self._username = user_data['username']
        self._email = user_data['email']
        self._salt = user_data['salt']

    @classproperty
    def is_logged(cls):
        return cls.logged_user is not None

    @classmethod
    def get_user(cls):
        return cls.logged_user

    @classmethod
    def login_user(cls, user_data):
        user = db_manager.get_user_if_exist(user_data)
        cls.logged_user = User(user)

    @classmethod
    def register_user(cls, user_data):
        new_user_id = db_manager.register_user(user_data)
        new_user = db_manager.get_user_by_id(new_user_id)
        cls.logged_user = User(new_user)
    
    @classmethod
    def logout_user(cls):
        del cls.logged_user
        cls.logged_user = None

    @classproperty
    def _id(cls):
        return cls.logged_user._id

    @classproperty
    def username(cls):
        return cls.logged_user._username

    @classproperty
    def email(cls):
        return cls.logged_user._email

    @classproperty
    def salt(cls):
        return cls.logged_user._salt

    @classproperty
    def get_auth_data(cls):
        return {
            '_id' : cls._id,
            'salt': cls.salt
        }