from ninja import NinjaAPI

api = NinjaAPI()

api.add_router("/blog/", "blog.api.router")
