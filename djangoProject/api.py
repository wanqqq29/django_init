from ninja import NinjaAPI, Router

api = NinjaAPI()
router = Router()


@router.get('/hello')
def hello(request):
    return {"message": "Hello World"}


api.add_router('', router)
