import falcon


class Resource(object):
    def on_get(self, req, resp):
        resp.body = '{"message": "Hello world!"}'
        resp.status = falcon.HTTP_200


class RetrieveData(object):
    def __init__(self):
        self.external_data = self.get_external_data()

    def get_external_data(self):
        import json
        import urllib2
        info = json.load(urllib2.urlopen(
            "http://redsky.target.com/v1/pdp/tcin/13860428?excludes=taxonomy,price,promotion,bulk_ship,rating_and_review_reviews,rating_and_review_statistics,question_answer_statistics"))

        print info['product']['available_to_promise_network']['product_id']