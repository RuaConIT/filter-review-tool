import uvicorn
from fastapi import FastAPI

from utils.base_route import BaseRoute


class APIApp():
    def __init__(self):
        self.app = FastAPI()
        self.base_route = BaseRoute.default_route(prefix='/process')
        self.app.include_router(self.base_route.router)

    def add_endpoint(self, endpoint: str, func, description: str, methods: [str],
                     request_data_model=None, response_data_model=None,
                     use_thread: bool = True, use_async: bool = True, **kwargs):

        self.base_route.add_endpoint(endpoint=endpoint, func=func, description=description,
                                     methods=methods, use_thread=use_thread, use_async=use_async,
                                     request_data_model=request_data_model,
                                     response_data_model=response_data_model, **kwargs)
        self.app.include_router(self.base_route.router)

    def start(self, n_workers: int = 1):
        uvicorn.run(self.app, host=self.config.api_host, port=self.config.api_port, reload=False, log_level="debug",
                    debug=False, workers=n_workers, factory=False, loop="asyncio", timeout_keep_alive=120)
