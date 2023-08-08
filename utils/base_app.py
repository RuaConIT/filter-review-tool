import logging
from utils.api_app import APIApp


class BaseApp():
    def __init__(self, config):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.config = config
        self.api_app = APIApp()

    def start(self, n_workers: int = 1):
        self.api_app.start(n_workers=n_workers)

    def join(self):
        self.api_app.start()


if __name__ == "__main__":
    app = BaseApp()
    app.start()
    app.join()

