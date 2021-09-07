'''SQLAlchemy models for CryptoTracker.'''

from datetime import datetime
from enum import unique

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class Tracked(db.Model):
    '''Relationship between users and coins'''
    __tablename__ = 'tracked'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade'),
    )

    coin_id = db.Column(
        db.Integer,
        db.ForeignKey('coins.id', ondelete='cascade'),
    )


class User(db.Model):
    '''User model'''
    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    fullname = db.Column(
        db.Text,
        nullable=False,
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

    tracking = db.relationship(
        'Tracking'
    )

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
