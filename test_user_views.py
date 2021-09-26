'''user views tests'''
import os
import json
from unittest import TestCase
from models import db, connect_db, User, Coin, Tracked
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


class UserViewTestCase(TestCase):
    '''test views for users'''
    def setUp(self):
        '''create test client, add sample data.'''
        User.query.delete()
        Tracked.query.delete()
        Coin.query.delete()
        self.client = app.test_client()

        test_user = User.signup(
            username='testuser',
            email='test@test.com',
            password='testuser')

        db.session.commit()
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

        self.testuser_id = test_user.id

    def tearDown(self):
        '''clean up fouled transactions'''

        db.session.rollback()

# detailed coin view
    def test_user_view_coin(self):
        '''can a logged in user see details about a coin?'''
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY]=self.testuser_id

        resp=c.get('/show/BTC', follow_redirects=True)
        html=resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('max supply', html)
    
    def test_user_view_coin_logged_out(self):
        '''can a logged out user see details about a coin?'''
        resp=self.client.get('/show/BTC', follow_redirects=True)
        html=resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('You must create an account and be logged in to do that!', html)

# track coin
    def test_user_track_coin(self):
        '''can a logged in user track then untrack a coin?'''
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY]=self.testuser_id

        resp1=c.post('/users/toggle_coin/BTC', follow_redirects=True)
        html=resp1.get_data(as_text=True)
        self.assertEqual(resp1.status_code, 200)
        self.assertIn('Coin has been added to your tracked coins.', html)
        resp2=c.post('/users/toggle_coin_off/BTC', follow_redirects=True)
        html=resp2.get_data(as_text=True)
        self.assertEqual(resp2.status_code, 200)
        self.assertIn('Coin has been removed from your tracked coins.', html)
    
    def test_user_track_coin_logged_out(self):
        '''can a logged out user track a coin?'''
        resp=self.client.post('/users/toggle_coin/BTC', follow_redirects=True)
        html=resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('You must create an account and be logged in to do that!', html)

# about - both logged in and out can view this page
    def test_user_view_about(self):
        '''can a logged in user view the about page?'''
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY]=self.testuser_id
        
        resp=self.client.get('/about', follow_redirects=True)
        html=resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('About Me', html)
    
    def test_user_view_about(self):
        '''can a logged out user view the about page?'''
        resp=self.client.get('/about', follow_redirects=True)
        html=resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('About Me', html)

# resources
    def test_user_view_resources(self):
        '''can a logged in user view the resources page?'''
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY]=self.testuser_id
        
        resp=self.client.get('/resources', follow_redirects=True)
        html=resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Cryptocurrency Guides, Exchanges and Wallets', html)        

    def test_user_view_resources_logged_out(self):
        '''can a logged out user view the resources page?'''
        resp=self.client.get('/resources', follow_redirects=True)
        html=resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('You must create an account and be logged in to do that!', html)

# login/logout
    def test_login(self):
        '''can a user login?'''
        user = User.query.get(self.testuser_id)

        with self.client as c:
            resp = c.post(
                '/login',
                data={
                    'username': user.username,
                    'password': 'testuser'
                },
                follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'Hello, {user.username}!', html)

    def test_logout(self):
        '''Can a user log out?'''

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY]=self.testuser_id
        resp = c.get(
            '/logout',
            follow_redirects=True)
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('You have been successfully logged out!', html)

    def test_login_fail(self):
        '''can a user log in with bad credentials?'''
        user = User.query.get(self.testuser_id)

        with self.client as c:
            resp = c.post(
                '/login',
                data={
                    'username': user.username,
                    'password': 'wrongpass'
                },
                follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Incorrect username or password!', html)

# delete account
    def test_user_delete_account(self):
        '''can a user be deleted?'''
        user = User.query.get(self.testuser_id)
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY]=self.testuser_id
            resp = c.post(
                '/delete',
                data={
                    'username': user.username,
                    'password': 'testuser'
                },
                follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Your account has been deleted!', html)

    def test_user_delete_account_fail(self):
        '''can a user be deleted with bad credentials?'''
        user = User.query.get(self.testuser_id)
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY]=self.testuser_id
            resp = c.post(
                '/delete',
                data={
                    'username': user.username,
                    'password': 'wrongpass'
                },
                follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Incorrect username or password!', html)