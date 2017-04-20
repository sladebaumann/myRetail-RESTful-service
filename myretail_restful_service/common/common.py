import falcon
import json
import redis
import urllib2

REDIS_DB = redis.StrictRedis(host='localhost', port=6379, db=0)

class Common(object):
    def get_external_api(self):
        # method simply loads json from external api and returns it
        try:
            info = json.load(urllib2.urlopen(
            "http://redsky.target.com/v1/pdp/tcin/13860428?excludes=taxonomy,"
            "price,promotion,bulk_ship,rating_and_review_reviews,"
            "rating_and_review_statistics,question_answer_statistics"))
        except Exception:
            raise falcon.HTTPError(
                "404 Object Not Found",
                description="External API url does not exist or "
                            "can't be found.")
        return info

    def verify_id_exists_in_external_api(self, id, info):
        # check if id that is passed it is in the external API
        if (info['product']['available_to_promise_network'][
                'product_id']) == id:
            return int(id)
        else:
            raise falcon.HTTPError(
                "400 Product {id} does not exist",
                description="Product {id} doesn't exist in external API. "
                            "Please make sure your URL is written correctly.")

    def verify_id_exists_in_database(self, id):
        # check if id passed is in database
        if REDIS_DB.hexists(id, "value"):
            return True
        else:
            raise falcon.HTTPError(
                "400 Product {id} does not exist",
                description="Product {id} doesn't exist in database. "
                            "Please make sure initial database entry "
                            "exists (see README.md)")
