from app import app
from models import db, Coin, User, Tracked
import json

db.drop_all()
db.create_all()

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
