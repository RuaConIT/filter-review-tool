from fastapi import File, UploadFile

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from config.config import Config
from controller.process_controller import ProcessorController


# Object define
class ReviewData(BaseModel):
    text: str = ""

    def __repr__(self):
        return self.text


def create_app(config: Config, multiprocess: bool = False):
    if multiprocess:
        raise NotImplementedError("Multiprocessing app not created")
    else:
        app = FastAPI()
        process_controller = ProcessorController(config=config)

        @app.post("/process")
        async def create_item(input_data: ReviewData):
            output = process_controller.run(input_data.text)
            return output

        return app


if __name__ == "__main__":
    _config = Config()
    _app = create_app(config=_config)
    uvicorn.run(_app, host=_config.api_host, port=_config.api_port)
