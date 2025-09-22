from fastapi import APIRouter, FastAPI

from project_template.example_blog import views

# 添加根路径路由
def root_router():
    router = APIRouter()
    
    @router.get("/", include_in_schema=False)
    async def root():
        return RedirectResponse(url="/docs")
    
    return router
    
def router_v1():
    router = APIRouter()
    router.include_router(views.router, tags=['Article'])
    return router


def init_routers(app: FastAPI):
    app.include_router(router_v1(), prefix='/api/v1', tags=['v1'])
