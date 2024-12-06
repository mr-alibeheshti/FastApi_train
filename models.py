import datetime as _datetime
import sqlalchemy as _sqlalchemy
import sqlalchemy.orm as _orm
import passlib.hash as _hash
import database as _database


class UserModel(_database.Base):
    __tablename__ = "users"
    id = _sqlalchemy.column(_sqlalchemy.Integer, primary_key=True, index=True)
    email = _sqlalchemy.column(_sqlalchemy.String, unique=True, index=True)
    name = _sqlalchemy.column(_sqlalchemy.String)
    phone = _sqlalchemy.column(_sqlalchemy.Integer)
    password_hash = _sqlalchemy.column(_sqlalchemy.String)
    created_at = _sqlalchemy.column(
        _sqlalchemy.Date, defualt=_datetime.datetime.utcnow())


class PostModel(_database.Base):
    __tablename__ = "posts"
    id = _sqlalchemy.column(_sqlalchemy.Integer, primary_key=True, index=True)
    user_id = _sqlalchemy.column(
        _sqlalchemy.Integer, _sqlalchemy.ForeignKey("users.id"))
    post_title = _sqlalchemy.column(_sqlalchemy.String, index=True)
    post_description = _sqlalchemy.column(_sqlalchemy.String, index=True)
    post_created_at = _sqlalchemy.column(_sqlalchemy.Date, defualt=_datetime.datetime.utcnow())
    
