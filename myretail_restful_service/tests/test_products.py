import falcon
import json
import mock
import unittest

from myretail_restful_service.common import exceptions
from myretail_restful_service.products import products

EXTERNAL_API_DICT = {
    "product": {
        "available_to_promise_network": {
            "product_id": "13860428", },
        "item": {
            "product_description": {
                "title": "The Big Lebowski (Blu-ray)", }
        }
    }
}


RETURNED_PRODUCT = {
    "id": 13860428, "name": "The Big Lebowski (Blu-ray) (Widescreen)",
    "current_price": {
        "value": 13.49, "currency_code": "USD"}
}


class TestProductsAPI(unittest.TestCase):
    def setUp(self):
        self.products = products.Resource()
        self.exceptions = exceptions.FalconExceptions()

    @mock.patch('myretail_restful_service.products.products.json.dumps')
    @mock.patch('myretail_restful_service.products.products.common')
    def test_on_get(self, common, json_dumps):
        json_dumps.return_value = RETURNED_PRODUCT
        req = mock.MagicMock()
        resp = falcon.Response()
        id = mock.MagicMock()
        products.Resource().on_get(req, resp, id)

        self.assertEqual(RETURNED_PRODUCT['id'], resp.body['id'])
        self.assertEqual(RETURNED_PRODUCT['name'], resp.body['name'])
        self.assertEqual(RETURNED_PRODUCT['current_price'],
                         resp.body['current_price'])

    @mock.patch('myretail_restful_service.products.products.common')
    def test_on_put(self, common):
        req = mock.MagicMock()
        req.stream.read.return_value = json.dumps(RETURNED_PRODUCT)
        resp = falcon.Response()
        id = mock.MagicMock()
        products.Resource().on_put(req, resp, id)

        self.assertEqual(
            'New Product Value Written to Database Successfully', resp.body)


class TestUpdateData(unittest.TestCase):
    def setUp(self):
        self.products = products.UpdateData()
        self.exceptions = exceptions.FalconExceptions()

    @mock.patch('myretail_restful_service.products.products.json.loads')
    def test_get_new_product_price_json_load(self, json_loads):
        json_loads.return_value = (
            {"current_price": {"currency_code": "USD", "value": 13.49}})
        product_name = mock.MagicMock()
        try:
            self.products.get_new_product_price(product_name)
        except:
            self.fail('Exception raised')

    @mock.patch('myretail_restful_service.products.products.json.loads')
    def test_get_failed_new_product_price_json_load(self, json_loads):
        json_loads.return_value = ['list', 'not', 'dict']
        product_name = mock.MagicMock()
        self.assertRaises(falcon.HTTPError,
                          self.products.get_new_product_price, product_name)


class TestRetrieveData(unittest.TestCase):
    def setUp(self):
        self.products = products.RetrieveData()
        self.exceptions = exceptions.FalconExceptions()

    @mock.patch('myretail_restful_service.products.products.common')
    @mock.patch('myretail_restful_service.common.common.REDIS_DB')
    def test_get_database_data(self, redis_db, common):
        id = mock.MagicMock()
        common.return_value = True
        redis_db.hgetall.return_value = (
            {"currency_code": "USD", "value": 13.49})
        expected_dict = (
            {'current_price': {'currency_code': 'USD', 'value': 13.49}})

        self.assertDictEqual(expected_dict,
                             self.products.get_database_data(id, redis_db))
