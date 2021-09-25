'''SQLAlchemy models for CryptoTracker.'''

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class Tracked(db.Model):
    '''Mapping relationship between users and coins'''
    __tablename__ = 'tracked'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade'),
    )

    coin_abbr = db.Column(
        db.Text,
        db.ForeignKey('coins.abbr', ondelete='cascade'),
    )


class User(db.Model):
    '''User model'''
    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    tracked = db.relationship(
        'Coin',
        secondary='tracked'
    )

    def __repr__(self):
        return f'<User #{self.id}: {self.username}, {self.email}>'

    @classmethod
    def signup(cls, username, email, password):
        '''Sign up a user
        Hashes password and adds user to system
        '''

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
        )

        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def authenticate(cls, username, password):
        '''Find a user with username and password

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        '''

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Coin(db.Model):
    '''Info for each individual coin from api'''
    __tablename__ = 'coins'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    name = db.Column(
        db.String,
        nullable=False,
        unique=True,
    )

    abbr = db.Column(
        db.String,
        nullable=False,
        unique=True,
    )


def connect_db(app):
    '''Connect db to Flask app'''
    db.app = app
    db.init_app(app)
