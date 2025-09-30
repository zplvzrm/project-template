"""server"""
import uvicorn
from fastapi import FastAPI

from project_template.example_blog import middlewares, routes
from project_template.config import settings
from project_template.log import init_log

app = FastAPI()
# 在模块级别初始化中间件和路由
middlewares.init_middleware(app)
routes.init_routers(app)

class Server:

    def __init__(self):
        init_log()
        self.app = app
        self.module_name = __name__

    # def init_app(self):
    #     middlewares.init_middleware(self.app)
    #     routes.init_routers(self.app)

    def run(self):
        # self.init_app()
        uvicorn.run(
            # app=self.app,
            # app="project_template.example_blog.server:app",
            app = f"{self.module_name}:app",
            host=settings.HOST,
            port=settings.PORT,
            reload=True, # bug,开启此功能需要将参数app设置为server:app，但如此设置后，接口文档页面为空
            workers=1
        )