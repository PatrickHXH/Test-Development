from ninja import  NinjaAPI
from manager.api import router as manager_router
from  app_api.api import router as api_router
api = NinjaAPI()

api.add_router("/manager/", manager_router)
api.add_router("/demo/", api_router)