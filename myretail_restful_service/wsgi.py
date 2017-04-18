from myretail_restful_service.app import SetupAPI
from myretail_restful_service.products.products import Resource

app = SetupAPI()
products = Resource()

app.api.add_route('/', products)
