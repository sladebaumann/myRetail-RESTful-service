import falcon


class FalconExceptions(object):
    def json_wrong_type(self):
        raise falcon.HTTPError(
            "400 json object malformed",
            description=("JSON object that was passed in the PUT "
                         "request appears to be of the wrong type. "
                         "Please make sure your URL is written correctly."))

    def json_incorrect_syntax(self):
        raise falcon.HTTPError(
            "400 json object malformed",
            description=("JSON object that was passed in the PUT "
                         "request appears to hold incorrect values "
                         "or isn't modeled after a typical GET "
                         "response.Please make sure your URL is "
                         "written correctly."))

    def external_api_not_found(self):
        raise falcon.HTTPError(
            "404 Object Not Found",
            description=("External API does not exist or can't be found."))

    def product_id_not_in_external_api(self):
        raise falcon.HTTPError(
            "400 Object Not Found",
            description=("Product {id} doesn't exist in external API. "
                        "Please make sure your URL is written correctly."))

    def product_id_not_in_database(self):
        raise falcon.HTTPError(
            "400 Object Not Found",
            description="Product {id} doesn't exist in database. "
                        "Please make sure initial database entry "
                        "exists (see README.md)"
        )

    def database_unreachable(self):
        raise falcon.HTTPError(
            "500 Internal Server Error",
            description="Redis database server unreachable. "
                        "Possible explanations may be incorrect port in redis "
                        "container or redis service isn't running."
        )