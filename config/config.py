import os

from common.common_keys import *


class Config():
    def __init__(self):
        self.pretrain_model = os.getenv(PRETRAIN_MODEL, "bert-base-uncased")
        self.checkpoint_path = os.getenv(CHECKPOINT_PATH, 'checkpoint/etsy-reviewer-model.pt')
        self.threshold = float(os.getenv(THRESHOLD, 0.75))
        self.api_port = int(os.getenv(API_PORT, 3030))
        self.api_host = os.getenv(API_HOST, '0.0.0.0')

