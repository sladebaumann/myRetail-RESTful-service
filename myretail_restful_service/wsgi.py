from myretail_restful_service.app import SetupAPI
from myretail_restful_service.products.products import Resource
from myretail_restful_service.products.products import RetrieveData

app = SetupAPI()
products = Resource()
external_data = RetrieveData()

app.api.add_route('/', products)
app.api.add_route('/data', external_data)
