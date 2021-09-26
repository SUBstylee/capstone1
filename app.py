import os

from flask import Flask, render_template, request, flash, redirect, session, g
# from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import AddUserForm, LoginForm
from models import db, connect_db, User, Coin, Tracked
##########################################################################
# api key is hidden here, make an account at 'nomics' for your own api key
from apikey import API_KEY
##########################################################################
import requests
import datetime
import time

CURR_USER_KEY = 'curr_user'
BASE_URL = 'https://api.nomics.com/v1'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///cryptotracker'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "654321")
# toolbar = DebugToolbarExtension(app)
connect_db(app)


# https://api.nomics.com/v1/markets?key=099d457c6b604422b5d11897e240647ae3d48437


############################
# Ticker - put this in a function because it would not update every page reload as a global variable


def ticker():
    return requests.get(
        url=f'{BASE_URL}/currencies/ticker?key={API_KEY}&interval=1d&per-page=10&page=1')


############################
# User signup/login/logout/delete


@app.before_request
def add_user_to_g():
    '''if logged in, add curr user to Flask Global'''
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    '''log in user'''
    session[CURR_USER_KEY] = user.id


def do_logout():
    '''log out user'''
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


def do_delete():
    '''delete a user's account'''
    do_logout()

    db.session.delete(g.user)
    db.session.commit()


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    '''handle user signup
    create new user and add to db, then redirect to home page
    if form not valid, present form again
    if user name is taken, flash message then re-present form
    '''
    form = AddUserForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
            )
            db.session.commit()

        except IntegrityError:
            flash('Username or Email already in use!', 'danger')
            return render_template('users/signup.html', form=form, api_ticker=ticker().json())

        do_login(user)

        return redirect('/')

    else:
        return render_template('users/signup.html', form=form, api_ticker=ticker().json())


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''handle user login'''
    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            do_login(user)
            flash(f'Hello, {user.username}!', 'success')
            return redirect('/')

        flash('Incorrect username or password!', 'danger')

    return render_template('users/login.html', form=form, api_ticker=ticker().json())


@app.route('/logout')
def logout():
    '''handle user logging out'''
    if not g.user:
        return redirect('/')
    do_logout()
    flash('You have been successfully logged out!', 'warning')
    return redirect('/')


@app.route('/delete', methods=['GET', 'POST'])
def delete_user():
    '''delete a user's account'''
    if not g.user:
        return redirect('/')
    # reuse login form to delete account
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            do_delete()
            flash('Your account has been deleted!', 'danger')
            return redirect('/')
        flash('Incorrect username or password!', 'danger')

    return render_template('users/delete.html', form=form, api_ticker=ticker().json())


############################
# User (must be logged in) track/untrack coins
@app.route('/users/toggle_coin/<coin_abbr>', methods=['POST'])
def toggle_tracked_coin(coin_abbr):
    '''toggle tracked coins from 'all' coins'''
    if not g.user:
        flash('You must create an account and be logged in to do that!', 'danger')
        return redirect('/signup')
    toggled = Coin.query.filter(Coin.abbr == coin_abbr).all()
    for track in g.user.tracked:
        if coin_abbr == track.abbr:
            g.user.tracked.remove(track)
            db.session.commit()
            flash('Coin has been removed from your tracked coins.', 'warning')
            return redirect('/allcoins')
    g.user.tracked.extend(toggled)
    db.session.commit()
    flash('Coin has been added to your tracked coins.', 'success')
    return redirect('/allcoins')


@app.route('/users/toggle_coin_off/<coin_abbr>', methods=['POST'])
def toggle_tracked_coin_off(coin_abbr):
    '''toggle tracked coins off from users tracked coins page (my coins) '''
    if not g.user:
        flash('You must create an account and be logged in to do that!', 'danger')
        return redirect('/signup')
    toggled = Coin.query.filter(Coin.abbr == coin_abbr).all()
    for track in g.user.tracked:
        if coin_abbr == track.abbr:
            g.user.tracked.remove(track)
            db.session.commit()
            flash('Coin has been removed from your tracked coins.', 'warning')
            return redirect('/')
    # Probably don't need this, but if somehow an untoggled coin shows up here, this will prevent crash
    g.user.tracked.extend(toggled)
    db.session.commit()
    flash('Coin has been added to your tracked coins.', 'success')
    return redirect('/')
############################
# Coin routes


@app.route('/allcoins')
def all_coins_list():
    '''show all coins to a logged in user'''
    if g.user:
        api_data = requests.get(
            url=f'{BASE_URL}/currencies/ticker?key={API_KEY}&interval=1d&per-page=100&page=1')
        time.sleep(1)
        return render_template('home-anon.html', api_data=api_data.json(), api_ticker=ticker().json(), Tracked=Tracked)
    else:
        return redirect('/')


@app.route('/show/<abbr>')
def coin_info(abbr):
    '''show more about an individual coin if user logged in, if anon then redirect to account creation page'''
    if g.user:
        hour = datetime.datetime.utcnow().hour
        today = datetime.datetime.utcnow().date()
        yesterday = today - datetime.timedelta(days=1)
        api_coin_data = requests.get(
            url=f'{BASE_URL}/currencies/ticker?key={API_KEY}&ids={abbr}'
        )
        time.sleep(1)
        api_spark_data = requests.get(
            url=f'{BASE_URL}/currencies/sparkline?key={API_KEY}&ids={abbr}&start={yesterday}T{hour}%3A00%3A00Z&end={today}T{hour}%3A00%3A00Z'
        )
        time.sleep(1)
        return render_template('/crypto/show.html', api_coin_data=api_coin_data.json(), api_ticker=ticker().json(), api_spark_data=api_spark_data.json())
    else:
        flash('You must create an account and be logged in to do that!', 'danger')
        return redirect('/signup')


# @app.route('/get-json')
# def coin_json():
#     '''get json for 'abbr' and 'name' for 300 highest ranked coins.  this is for purposes of seeding the database, so this route will be commented out.  only use when updating database is needed.  probably don't need 300, but included them in case some coins suddenly gain popularity, and won't have to update database so often.  always chance of a new coin emerging and entering top 100, so if that happens and breaks app, update database with this as well...'''
#     api_coin_data1 = requests.get(
#         url=f'{BASE_URL}/currencies/ticker?key={API_KEY}&interval=1d&per-page=100&page=1'
#     )
#     time.sleep(1)
#     api_coin_data2 = requests.get(
#         url=f'{BASE_URL}/currencies/ticker?key={API_KEY}&interval=1d&per-page=100&page=2'
#     )
#     time.sleep(1)
#     api_coin_data3 = requests.get(
#         url=f'{BASE_URL}/currencies/ticker?key={API_KEY}&interval=1d&per-page=100&page=3'
#     )
#     time.sleep(1)
#     return render_template('/crypto/get-json.html', api_coin_data1=api_coin_data1.json(), api_coin_data2=api_coin_data2.json(), api_coin_data3=api_coin_data3.json(), api_ticker=ticker().json())

############################
# About and Resources


@app.route('/about')
def about_page():
    '''show about page - general information'''
    return render_template('about.html', api_ticker=ticker().json())


@app.route('/resources')
def resources_page():
    '''show resources page - external links
    requires users to be logged in because some of these resources contain financial/investment advice
    user needs to agree to disclaimer
    '''
    if not g.user:
        flash('You must create an account and be logged in to do that!', 'danger')
        return redirect('/signup')
    return render_template('resources.html', api_ticker=ticker().json())

############################
# Home and error pages


@app.route('/')
def homepage():
    '''Shows homepage

    - anon users: see list of all coins and sign up/login links
    - logged in users: see list of followed coins and all coins/logout/delete user links
    '''
    display_coins = []
    if g.user:

        tracked = (Tracked.query.all())
        for track in tracked:
            if track.user_id == g.user.id:
                display_coins.append(track.coin_abbr)
        if len(display_coins) < 1:
            return render_template('home.html', api_ticker=ticker().json())
        else:
            api_tracked_data = requests.get(
                url=f'{BASE_URL}/currencies/ticker?key={API_KEY}&ids={",".join(display_coins)}&interval=1d&per-page=100&page=1'
            )
        time.sleep(1)
        return render_template('home.html', api_tracked_data=api_tracked_data.json(), api_ticker=ticker().json(), Tracked=Tracked)
    else:
        api_data = requests.get(
            url=f'{BASE_URL}/currencies/ticker?key={API_KEY}&interval=1d&per-page=100&page=1')
        time.sleep(1)
        return render_template('home-anon.html', api_data=api_data.json(), api_ticker=ticker().json(), Tracked=Tracked)

##############################################################################
# Turn off all caching in Flask
#   (useful for dev; in production, this kind of stuff is typically
#   handled elsewhere)
#
# https://stackoverflow.com/questions/34066804/disabling-caching-in-flask


@ app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req
