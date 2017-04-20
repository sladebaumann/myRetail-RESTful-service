import json
import urllib2

class Common(object):
    def get_external_api(self):
        # method simply loads json from external api and returns it
        info = json.load(urllib2.urlopen(
            "http://redsky.target.com/v1/pdp/tcin/13860428?excludes=taxonomy,price,promotion,bulk_ship,rating_and_review_reviews,rating_and_review_statistics,question_answer_statistics"))
        return info

    def verify_id_exists(self, id, info):
        # check if id that is passed it is in the external API
        if (info['product']['available_to_promise_network'][
                'product_id']) == id:
            return int(id)
            # TODO: put falcon error handling in here in an else statement)
            # aka return failure or something here. If it doesn't find
            # ID, then falc on should return "missing ID"