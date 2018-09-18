import uuid

import requests
from bs4 import BeautifulSoup
import re
import src.models.items.constants as ItemConstants

from src.common.database import Database
from src.models.stores.store import Store


class Item(object):
    def __init__(self, name, url, price=None, _id=None):
        self.name = name
        self.url = url
        store = Store.get_by_url(url)
        self.tag_name = store.tag_name
        self.query = store.query
        # tag_name = store.tag_name
        # query = store.query
        # self.price = self.load_item(tag_name, query)
        self.price = None if price is None else price
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Item {} with URL {}>".format(self.name, self.url)

    # def load_item(self, tag_name, query):
    #     # <div class="_1vC4OE _3qQ9m1">₹55,069</div>
    #     request = requests.get(self.url)
    #     content = request.content
    #     soup = BeautifulSoup(content,"html.parser")
    #     element = soup.find(tag_name, query)
    #     print(element)
    #     string_price = element.text.strip()
    #
    #     pattern = re.compile("(\d+.\d+)")
    #     match = pattern.search(string_price)
    #
    #     return match.group()

    def load_price(self):
        # <div class="_1vC4OE _3qQ9m1">₹55,069</div>
        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(content,"html.parser")
        element = soup.find(self.tag_name, self.query)
        # print(element)
        string_price = element.text.strip()

        pattern = re.compile("(\d+.\d+)")
        match = pattern.search(string_price)
        self.price = float(match.group().replace(",", ""))

        return self.price

    def save_to_mongo(self):
        # Database.insert(ItemConstants.COLLECTION, self.json())
        Database.update(ItemConstants.COLLECTION, {"_id": self._id}, self.json())

    # def from_mongo(self):
    #     Database.find_one(ItemConstants.COLLECTION, {"name":self.name})

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            # "store": self.store,
            "url": self.url,
            "price": self.price
        }

    @classmethod
    def find_by_item_id(cls, item_id):
        return cls(** Database.find_one(ItemConstants.COLLECTION, {"_id": item_id}))