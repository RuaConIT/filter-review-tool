import torch
import random
import numpy as np
from transformers import BertTokenizer, BertModel

from bertgru_sentiment import BERTGRUSentiment
from utils.base_singleton import BaseSingleton
from controller.session.process_session import ProcessSession


class ProcessorController(BaseSingleton):
    def __init__(self, config):
        super(ProcessorController, self).__init__()

        self.config = config
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        # tokenizer config
        self.tokenizer = BertTokenizer.from_pretrained(self.config.pretrain_model)
        self.init_token_idx = self.tokenizer.convert_tokens_to_ids(self.tokenizer.cls_token)
        self.eos_token_idx = self.tokenizer.convert_tokens_to_ids(self.tokenizer.sep_token)
        self.pad_token_idx = self.tokenizer.convert_tokens_to_ids(self.tokenizer.pad_token)
        self.unk_token_idx = self.tokenizer.convert_tokens_to_ids(self.tokenizer.unk_token)
        self.max_input_length = self.tokenizer.max_model_input_sizes[self.config.pretrain_model]

        # model config
        self.hidden_dim = 256
        self.output_dim = 1
        self.n_layers = 2
        self.bidirectional = True
        self.dropout = 0.25
        self.model = None

        # load model
        self.base_config()
        self.load_model()

    def run(self, text):
        session = self.create(
            config=self.config,
            model=self.model,
            tokenizer=self.tokenizer,
            max_input_length = self.max_input_length,
            init_token_idx=self.init_token_idx,
            eos_token_idx=self.eos_token_idx,
            device=self.device,
            text=text
        )

        session.start()
        session.join()

        return session.output

    def load_model(self):
        bert = BertModel.from_pretrained(self.config.pretrain_model)
        self.model = BERTGRUSentiment(
            bert,
            self.hidden_dim,
            self.output_dim,
            self.n_layers,
            self.bidirectional,
            self.dropout
        )

        self.model.load_state_dict(torch.load(
            self.config.checkpoint_path,
            map_location=torch.device(self.device)),
            strict=False
        )

    @staticmethod
    def base_config():
        seed = 1234
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        torch.backends.cudnn.deterministic = True

    @staticmethod
    def create(config, model, tokenizer, max_input_length, init_token_idx, eos_token_idx, device, text):
        return ProcessSession(config, model, tokenizer, max_input_length, init_token_idx, eos_token_idx, device, text)

