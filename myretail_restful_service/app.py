import falcon
import logging

LOGGER = logging.getLogger(__name__)


class SetupAPI(object):
    def __init__(self):
        self.api = self.make_api()

    def make_api(self):
        """Create falcon api
        """
        api = falcon.API()
        return api
