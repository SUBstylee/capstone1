'''user model tests'''
import os
import json
from unittest import TestCase
from models import db, connect_db, User, Coin, Tracked
from flask_bcrypt import Bcrypt
# needed for testing unique value error
from sqlalchemy.exc import IntegrityError
# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database
os.environ['DATABASE_URL'] = 'postgresql:///cryptotracker-test'
# Now we can import app
from app import app, CURR_USER_KEY
# don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
# Flask errors are real errors, instead of HTML pages with error info
app.config['TESTING'] = True
# turn off debugtoolbar intercept redirects
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data
db.create_all()
# don't have WTForms use CSRF at all, since it's a pain to test
app.config['WTF_CSRF_ENABLED'] = False
# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data
db.create_all()
bcrypt = Bcrypt()
U_DATA1 = {
    'email': 'test1@test.com',
    'username': 'testuser1',
    'password': 'HASHED_PASSWORD1'
}

U_DATA2 = {
    'email': 'test2@test.com',
    'username': 'testuser2',
    'password': 'HASHED_PASSWORD2'
}

class UserModelTestCase(TestCase):
    '''test tracked coins'''

    def setUp(self):
        '''create test client, add sample data'''
        User.query.delete()
        Tracked.query.delete()
        Coin.query.delete()
        self.client = app.test_client()

        u = User(**U_DATA1)
        u2 = User(**U_DATA2)

        db.session.add(u)
        db.session.commit()
        # changed this to storing self.user_id instead of the instance itself
        ##############
        self.user = u
        self.user2 = u2
        ##############
        # seed the database with coins
        f = open('static/json/coins.json',)
        data = json.load(f)
        for i in data:
            coin = Coin(
                name=i['name'],
                abbr=i['abbr'],
            )
            db.session.add(coin)
            db.session.commit()

        f.close()
    
    def tearDown(self):
        '''clean up fouled transactions'''
        db.session.rollback()

    def test_user_model(self):
        '''does basic model work?'''
        # user should not be tracking any coins yet
        self.assertEqual(len(self.user.tracked), 0)

    def test_user_signup(self):
        '''does User.create sucessfully create a new user given valid credentials?'''
        new_signup=User.signup(**U_DATA2)
        db.session.commit()

        self.assertIsInstance(new_signup.id, int)
        self.assertEqual(User.query.count(),2)

    def test_user_signup_fail(self):
        '''does User.create fail to create a new user if any of the validations (uniqueness, non-nullable fields...) fail?'''
        # signup fails if required value left empty
        U_DATA2.pop('username')
        with self.assertRaises(TypeError):
            new_user=User.signup(**U_DATA2)

        self.assertEqual(User.query.count(), 1)

        # signup fails if username not unique
        U_DATA2['username'] = U_DATA1['username']
        with self.assertRaises(IntegrityError):
            new_user=User.signup(**U_DATA2)
            db.session.add(new_user)
            db.session.commit()

        db.session.rollback()
        self.assertEqual(User.query.count(), 1)

    def test_user_authenticate(self):
        '''does User.authenticate sucessfully return a user when given a valid username and password?  Does it fail to return a user when the username or password is invalid?'''
        # needed to hash password and compare
        pw = U_DATA2['password']
        U_DATA2['password']=bcrypt.generate_password_hash(U_DATA2['password']).decode('UTF-8')
        new_user=User(**U_DATA2)

        db.session.add(new_user)
        db.session.commit()
        # test if authenticate is successful with correct username and password
        self.assertEqual(User.authenticate(U_DATA2['username'],pw),new_user)
        # test if authenticate fails on wrong password
        self.assertFalse(User.authenticate(U_DATA2['password'], 'wrongpass'))
        # test if suthenticate fails on wrong username
        self.assertFalse(User.authenticate('wrongusername', pw))