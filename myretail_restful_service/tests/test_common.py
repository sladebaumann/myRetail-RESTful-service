import falcon
import mock
import redis
import unittest

from myretail_restful_service.common import common, exceptions


class TestCommon(unittest.TestCase):
    def setUp(self):
        self.common = common.Common()
        self.exceptions = exceptions.FalconExceptions()

    @mock.patch('myretail_restful_service.common.common.json.load')
    def test_get_external_api_json_load(self, json_load):
        json_load.side_effect = None
        try:
            self.common.get_external_api()
        except:
            self.fail('Exception raised')

    @mock.patch('myretail_restful_service.common.common.json.load')
    def test_get_failed_external_api_json_load(self, json_load):
        json_load.side_effect = Exception
        self.assertRaises(falcon.HTTPError,
                          self.common.get_external_api)

    def test_verify_id_exists_in_external_api(self):
        id = 12345
        dictionary = (
            {"product": {
                "available_to_promise_network": {"product_id": id}}})
        new_id = self.common.verify_id_exists_in_external_api(id, dictionary)

        self.assertEqual(id, new_id)

    def test_verify_id_does_not_exist_in_external_api(self):
        id = 12345
        incorrect_id = 999
        dictionary = (
            {"product": {"available_to_promise_network": {
                "product_id": incorrect_id}}})

        self.assertRaises(falcon.HTTPError,
                          self.common.verify_id_exists_in_external_api,
                          id, dictionary)

    @mock.patch('myretail_restful_service.common.common.REDIS_DB')
    def test_verify_id_exists_in_database(self, mock_redis_db):
        mock_redis_db.hexists.return_value = True
        id = mock.MagicMock()

        self.assertTrue(self.common.verify_id_exists_in_database(id))

    @mock.patch('myretail_restful_service.common.common.REDIS_DB')
    def test_verify_id_does_not_exist_in_database(self, mock_redis_db):
        mock_redis_db.hexists.return_value = False
        id = mock.MagicMock()

        self.assertRaises(falcon.HTTPError,
                          self.common.verify_id_exists_in_database, id)

    @mock.patch('myretail_restful_service.common.common.REDIS_DB')
    def test_verify_successful_redis_connection(self, mock_redis_db):
        mock_redis_db.ping.side_effect = None
        try:
            self.common.verify_successful_redis_connection()
        except:
            self.fail('Exception raised')

    @mock.patch('myretail_restful_service.common.common.REDIS_DB')
    def test_unsuccessful_redis_connection(self, mock_redis_db):
        mock_redis_db.ping.side_effect = redis.ConnectionError
        self.assertRaises(falcon.HTTPError,
                          self.common.verify_successful_redis_connection)
