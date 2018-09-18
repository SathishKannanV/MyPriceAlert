import datetime
import uuid

import requests
import src.models.alerts.constants as AlertConstants
from src.common.database import Database
from src.models.items.item import Item



class Alert(object):
    def __init__(self, user_email, price_limit, item_id, active=True, last_checked=None, _id=None):
        self.user_email = user_email
        self.price_limit = price_limit
        self.item = Item.find_by_item_id(item_id)
        self.active = active
        self.last_checked = datetime.datetime.utcnow() if last_checked is None else last_checked
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Alert for {} on item {} with price of {}>".format(self.user_email, self.item.name , self.price_limit)

    def send_mail(self):
        return requests.post(
            AlertConstants.URL,
            auth=("api", AlertConstants.API_KEY),
            data={
                "from": AlertConstants.FROM,
                "to": self.user_email,
                "subject": "Price have dropped for {} item".format(self.item.name),
                "text": "It is time to grab the deal!! (link: {})".format(self.item.url, "http://pricing.sample.com/alerts/{}".format(self._id))
            }
        )

    @classmethod
    def find_needing_updates(cls, min_last_update = AlertConstants.ALERT_TIMEOUT):
        last_updated = datetime.datetime.utcnow() - datetime.timedelta(minutes=min_last_update)
        return [cls(**ele) for ele in Database.find(AlertConstants.COLLECTION, {"last_checked": {"$lte": last_updated},
                                                                                "active": True})]

    def save_to_mongo(self):
        # Database.insert(AlertConstants.COLLECTION, self.json())
        Database.update(AlertConstants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        return {
            "_id": self._id,
            "item_id": self.item._id,
            "price_limit": self.price_limit,
            "user_email": self.user_email,
            "last_checked": self.last_checked,
            "active": self.active
        }

    def load_item_price(self):
        self.item.load_price()
        self.item.save_to_mongo()
        self.last_checked = datetime.datetime.utcnow()
        self.save_to_mongo()
        return self.item.price

    def send_email_if_price_reached(self):
        if self.item.price < self.price_limit:
            self.send_mail()

    @classmethod
    def find_by_email(cls, user_email):
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTION, {"user_email": user_email})]


    @classmethod
    def find_by_id(cls, alert_id):
        return cls(**Database.find_one(AlertConstants.COLLECTION, {"_id": alert_id}))


    def deactivate(self):
        self.active = False
        self.save_to_mongo()

    def activate(self):
        self.active = True
        self.save_to_mongo()

    def delete(self):
        Database.remove(AlertConstants.COLLECTION, {"_id": self._id})
