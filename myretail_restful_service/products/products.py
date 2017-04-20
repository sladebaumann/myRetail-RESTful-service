import falcon
import json
import redis
import urllib2

from collections import OrderedDict


class Resource(object):
    def on_get(self, req, resp, id):
        product = RetrieveData()
        resp.body = json.dumps(product.get_combined_data(id))
        resp.status = falcon.HTTP_200
    #on_post will go here most likely


class RetrieveData(object):
    def get_external_data(self, id):
        external_dict = {}
        info = json.load(urllib2.urlopen(
            "http://redsky.target.com/v1/pdp/tcin/13860428?excludes=taxonomy,price,promotion,bulk_ship,rating_and_review_reviews,rating_and_review_statistics,question_answer_statistics"))

        # check if id that is passed it is in the external API
        if (info['product']['available_to_promise_network'][
            'product_id']) == id:
            self.product_id = int(id)
            # TODO: put falcon error handling in here in an else statement)
            # aka return failure or something here. If it doesn't find
            # ID, then falcon should return "missing ID"
        title = (info['product']['item']['product_description']['title'])

        external_dict['id'] = self.product_id
        external_dict['name'] = title

        return external_dict

    def get_database_data(self, id):
        price_dict = {}
        # use id from URL
        # hardcoded value inside redis db for now.
        # TODO: Will write code when post/database manipulation is setup
        # Using HMSET to set value based on 'id' being the key
        # and the values must go in reverse order as you want printed
        # `redis-cli HMSET 13860428 currency_code USD value 13.49`
        # `redis-cli HGETALL 13860428`
        redis_db = redis.StrictRedis(host='localhost', port=6379, db=0)
        # redis command to get entire hash (dict in python) based on id
        current_price = redis_db.hgetall(id)
        # convert price from string that redis stores to float
        current_price['value'] = float(current_price['value'])
        price_dict['current_price'] = current_price

        return price_dict


    def get_combined_data(self, id):
        external_data = self.get_external_data(id)
        database_data = self.get_database_data(id)
        combined_data = {}

        # combine data into one dict
        for data in (external_data,database_data):
            combined_data.update(data)

        # order the dict using OrderedDict for output
        key_order = ('id', 'name', 'current_price')
        ordered_combined_data = OrderedDict(
            (k, combined_data[k]) for k in key_order)
        return ordered_combined_data