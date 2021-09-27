# CryptoTracker

![cryptotracker logo](https://jt-cryptotracker.herokuapp.com/static/images/favicon_io/android-chrome-512x512.png)

CryptoTracker - designed to provide basic information about the top 100 cryptocurrencies by market cap.

This project was completed in approximately 40 hours as part of the Springboard Software Engineering fellowship program.

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

### Registration and Login

### Logout and Delete Account

### Top 10 Cryptocurrencies Ticker

### Top 100 Cryptocurrencies

### User Tracked Coins

### Detailed Coin Information

### About

### Resources

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

Tests were written for Models and Views using Python's build in [Unit Test](https://docs.python.org/3/library/unittest.html) Framework