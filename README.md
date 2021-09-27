# CryptoTracker

![cryptotracker logo](https://jt-cryptotracker.herokuapp.com/static/images/favicon_io/android-chrome-512x512.png)

CryptoTracker - designed to provide basic information about the top 100 cryptocurrencies by market cap.

This project was completed in approximately 50 hours as part of the Springboard Software Engineering fellowship program.

## Table of Contents

---

1. [Technologies Used](#technologies-used)
    * [Front End](#front-end)
    * [Back End](#back-end)
    * [Database](#database)
    * [API](#api)
    * [Data](#data)
    * [Graphic Design](#graphic-design)
2. [Deployment](#deployment)
3. [Developer](#developer)
4. [Promo/Demo Video](#promodemo-video)
5. [Demo Account for Site Use](#demo-account-for-site-use)
6. [Features](#features)
    * [Navigation Bar](#navigation-bar)
    * [Registration and Login](#registration-and-login)
    * [Logout and Delete Account](#logout-and-delete-account)
    * [Top 10 Cryptocurrencies Ticker](#top-10-cryptocurrencies-ticker)
    * [Top 100 Cryptocurrencies](#top-100-cryptocurrencies)
    * [User Tracked Coins](#user-tracked-coins)
    * [Detailed Coin Information](#detailed-coin-information)
    * [About](#about)
    * [Resources](#resources)
1. [Further Steps](#further-steps)
1. [Local Deployment](#local-deployment)
1. [Testing](#testing)

## Technologies Used

---

#### Front End:

HTML, HTML Canvas, CSS, BootStrap, JavaScript, Chart.js

#### Back End:

Python, Flask, SQLALchemy, WTForms, BCrypt, Jinja

#### Database:

PostgreSQL

#### API:

#### nomics api (free version)

Get your own free api key: [nomics](https://p.nomics.com/cryptocurrency-bitcoin-api)

View the docs: [nomics docs](https://nomics.com/docs/)

#### Data:

JSON file containing top 300 cryptocurrencies for seeding.  There is code included to update the JSON file in case a new coin comes along that makes the top 100, or an existing coin that is currently around and not on the top 300 gains enough of a market cap to get on the top 100 (unlikely, but possible).  In these two scenarios, update the JSON file and reseed the Coin table (NOT THE User OR Tracked TABLES!).  This should not affect the other tables as the tracked coins are based on coin abbreviation (abbr), not ID, which will persist even if ID changes.  Because of this, even if a coin drops off the top 100, a user already tracking it will continue doing so until they remove it from their tracked coins.

#### Graphic Design:

Photoshop, Illustrator, Camtasia

## Deployment

---

This app is currently deployed on Heroku at [CryptoTracker (https://jt-cryptotracker.herokuapp.com)](https://jt-cryptotracker.herokuapp.com/)

## Developer

---

### [Jeremy Threlfall](https://github.com/SUBstylee)

---

![Jeremy Threlfall](https://jt-cryptotracker.herokuapp.com/static/images/jeremy.png)

[LinkedIn](https://www.linkedin.com/in/jeremy-threlfall/)

Email: [jjthrelfall@gmail.com](mailto:jjthrelfall@gmail.com)

## Promo/Demo Video

---

[Promo/Demo Video of app](https://jt-cryptotracker.herokuapp.com/static/video/cryptotracker.mp4)
### API - [nomics](https://p.nomics.com/cryptocurrency-bitcoin-api)

## Demo Account for Site Use

---

This app uses User Registration and Login with Authentication to gain access to all features.  If you do not wish to make an account you can use the demo user account below:

Username: demouser

Password: demouser

## Features

---

### Navigation Bar

* The 'Navbar Brand Logo' routes a **LOGGED OUT** user to landing page (Top 100).  A **LOGGED IN** user is routed to their tracked coins.
* 'About' is about the developer (me).
* 'Resources' contains useful external links about cryptocurrency, exchanges, and wallets. **LOGGED IN** as some of the links contain financial/investment advice. 
* 'My Coins' routes a **LOGGED IN** user to their tracked coins.  A **LOGGED OUT** user cannot see this link or access this route.
* 'All Coins' routes a **LOGGED IN** user to the Top 100 list.  A **LOGGED OUT** user cannot see this link or access this route.
* 'User' drop down:
    * **LOGGED OUT**
        * 'Sign up'
        * 'Log in'
    * **LOGGED IN**
        * 'Logout'
        * 'Delete Account'

![nav](https://raw.githubusercontent.com/SUBstylee/capstone1/main/static/images/readme/nav.png)

### Registration and Login

The user registration page collects a minimal amount of information about the user.  This is keeping with the decentralized anonymous nature of cryptocurrencies.

The username and email must be unique, and the password must be six characters or more.  The user must also agree to the disclaimer by activating the checkbox.

User information is stored in the User table, and the password is hashed and salted using BCrypt.

![registration](https://raw.githubusercontent.com/SUBstylee/capstone1/main/static/images/readme/register.png)

User must use a preregistered username (unique) and correct password to gain access to full site.

![login](https://raw.githubusercontent.com/SUBstylee/capstone1/main/static/images/readme/login.png)

### Logout and Delete Account

User can logout on a single click.

![logout](https://raw.githubusercontent.com/SUBstylee/capstone1/main/static/images/readme/logout.png)

To delete an account, a user must be logged in, and credentials must be correct.  If these parameters are met, user and their tracked coins are dropped from corresponding tables.

![delete account](https://raw.githubusercontent.com/SUBstylee/capstone1/main/static/images/readme/delete.png)

### Top 10 Cryptocurrencies Ticker

This is a scrolling ticker that displays the latest information for the top ten cryptocurrencies.  It, like the navigation bar, appears on every route.

![ticker](https://raw.githubusercontent.com/SUBstylee/capstone1/main/static/images/readme/ticker.png)

### Top 100 Cryptocurrencies

This is a table that shows the top 100 cryptocurrencies. This appears on the landing page for a **LOGGED OUT** user.  A **LOGGED IN** user will see this in the 'All Coins' route.

![top 100](https://raw.githubusercontent.com/SUBstylee/capstone1/main/static/images/readme/top.png)

### User Tracked Coins

This is a table that shows a **LOGGED IN** users tracked coins.  A **LOGGED OUT** user cannot access this route.

![tracked](https://raw.githubusercontent.com/SUBstylee/capstone1/main/static/images/readme/tracked.png)

### Detailed Coin Information

This shows detailed information about individual coins.  Only a **LOGGED IN** user has access to these routes.

![detailed](https://raw.githubusercontent.com/SUBstylee/capstone1/main/static/images/readme/detailed.png)

### About

This shows information about the developer (me). **LOGGED OUT** and **LOGGED IN** users have access to this route.

![about](https://raw.githubusercontent.com/SUBstylee/capstone1/main/static/images/readme/about.png)

### Resources

This contains useful external links about cryptocurrency, exchanges, and wallets. Only a **LOGGED IN** user has access to this route as some of the links contain financial/investment advice.

![resources](https://raw.githubusercontent.com/SUBstylee/capstone1/main/static/images/readme/resources.png)

## Further Steps

---

I would have liked to make it so that a user could receive a notification when a tracked coin reaches a certain value.  Unfortunately, this would require constant (every few seconds) API calls that would flag my free API key and block.  If I were using a paid API key, then I could accomplish this by implementing an email system or using the Twillio API for sms notifications.

I also would have liked to make the sparkline chart into a candlestick chart, but again, the free version of the nomics API does not provide the information required for this.

I was thinking about requiring more information and allowing users to edit their information, but due to the nature of cryptocurrencies being decentralized, I decided to go minimalistic with data collected about a user.

Any feedback is appreciated.  Feel free to reach out or connect with me using the information listed under [Developer](#developer).

## Local Deployment

---

### Requirements:

Python, Pip, PostgreSQL

### API Key:

Register for a free API key from [nomics](https://p.nomics.com/cryptocurrency-bitcoin-api)

### Deploy locally using Python 3.8.5, pip, and Flask:

Initialize PostgreSQL in your operating system: [WSL2/Linux](https://docs.microsoft.com/en-us/windows/wsl/tutorials/wsl-database), [Mac](https://www.sqlshack.com/setting-up-a-postgresql-database-on-mac/)

Run the following commands in your terminal:

### Clone Repository, Enter Directory of Repo, and Make '`apikey.py`' File With Echo using your API key

`git clone https://github.com/SUBstylee/capstone1.git`

`cd capstone1`

`echo "API_KEY = 'YOUR_API_KEY_HERE'" > apikey.py`

### Create and Activate Python Virtual Environment

`python3 -m venv venv`

`source venv/bin/activate`

`pip3 install -r requirements.txt` or `pip install -r requirements.txt`

### To Set Up Our Local Database:

`createdb cryptotracker`

`python3 seed.py`

### Run Application With Flask

`export FLASK_ENV=production`

`export FLASK_RUN_PORT=8000`

`flask run`

### View Application in your Web Browser

Open the application in your web browser at [http://localhost:8000/](http://localhost:8000/)

## Testing

---

Tests were written for Models and Views using Python's built in [Unit Test](https://docs.python.org/3/library/unittest.html) Framework
