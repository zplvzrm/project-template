"""server"""
import uvicorn
from fastapi import FastAPI

from project_template.example_blog import middlewares, routes
from project_template.config import settings
from project_template.log import init_log


class Server:

    def __init__(self):
        init_log()
        self.app = FastAPI()

    def init_app(self):
        middlewares.init_middleware(self.app)
        routes.init_routers(self.app)

    def run(self):
        self.init_app()
        uvicorn.run(
            app=self.app,
            host=settings.HOST,
            port=settings.PORT,
        )