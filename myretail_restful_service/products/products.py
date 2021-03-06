import falcon
import json

from collections import OrderedDict
from myretail_restful_service.common import common, exceptions


class Resource(object):
    def on_get(self, req, resp, id):
        redis_db = common.Common().verify_successful_redis_connection()
        product = RetrieveData()
        resp.body = json.dumps(product.get_combined_data(id, redis_db))
        resp.status = falcon.HTTP_200

    def on_put(self, req, resp, id):
        redis_db = common.Common().verify_successful_redis_connection()
        new_product = req.stream.read()
        write_data = UpdateData().write_price_to_db(id, new_product, redis_db)
        resp.body = write_data
        resp.status = falcon.HTTP_200


class UpdateData(object):
    def write_price_to_db(self, id, new_product, redis_db):
        new_value = self.get_new_product_price(new_product)
        external_api = common.Common().get_external_api()
        product_id = common.Common().verify_id_exists_in_external_api(
            id, external_api)
        common.Common().verify_id_exists_in_database(id)
        redis_db.hset(product_id, "value", new_value)
        return ('New Product Value Written to Database Successfully')

    def get_new_product_price(self, new_product):
        try:
            return json.loads(new_product)["current_price"]["value"]
        except Exception:
            exceptions.FalconExceptions().json_wrong_type()


class RetrieveData(object):
    def get_external_data(self, id):
        external_dict = {}
        # get external api from common method
        external_api = common.Common().get_external_api()
        # check if id that is passed it is in the external API
        # and return product_id
        product_id = common.Common().verify_id_exists_in_external_api(
            id, external_api)
        title = (
            external_api['product']['item']['product_description']['title'])

        external_dict['id'] = product_id
        external_dict['name'] = title

        return external_dict

    def get_database_data(self, id, redis_db):
        price_dict = {}
        # use id from URL
        if common.Common().verify_id_exists_in_database(id):
            current_price = redis_db.hgetall(id)
            # convert price from string that redis stores to float
            current_price['value'] = float(current_price['value'])
            price_dict['current_price'] = current_price

            return price_dict

    def get_combined_data(self, id, redis_db):
        external_data = self.get_external_data(id)
        database_data = self.get_database_data(id, redis_db)
        combined_data = {}

        # combine data into one dict
        for data in (external_data, database_data):
            combined_data.update(data)

        # order the dict using OrderedDict for output
        key_order = ('id', 'name', 'current_price')
        ordered_combined_data = OrderedDict(
            (k, combined_data[k]) for k in key_order)
        return ordered_combined_data
