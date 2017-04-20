import json
import redis
import urllib2

from myretail_restful_service.common import exceptions

REDIS_DB = redis.StrictRedis(host='localhost', port=6379, db=0)


class Common(object):
    def get_external_api(self):
        # method simply loads json from external api and returns it
        try:
            info = json.load(urllib2.urlopen(
                "http://redsky.target.com/v1/pdp/tcin/13860428?"
                "excludes=taxonomy,price,promotion,bulk_ship,rating"
                "_and_review_reviews,rating_and_review_statistics,"
                "question_answer_statistics"))
        except Exception:
            exceptions.FalconExceptions().external_api_not_found()
        else:
            return info

    def verify_id_exists_in_external_api(self, id, info):
        # check if id that is passed it is in the external API
        if (info['product']['available_to_promise_network'][
                'product_id']) == id:
            return int(id)
        else:
            exceptions.FalconExceptions().product_id_not_in_external_api()

    def verify_id_exists_in_database(self, id):
        # check if id passed is in database
        if REDIS_DB.hexists(id, "value"):
            return True
        else:
            exceptions.FalconExceptions().product_id_not_in_database()

    def test_redis_connection(self):
        # verify redis server is active
        try:
            REDIS_DB.ping()
        except redis.ConnectionError:
            exceptions.FalconExceptions().database_unreachable()
        else:
            return REDIS_DB
