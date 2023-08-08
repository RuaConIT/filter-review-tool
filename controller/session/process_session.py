import torch
from threading import Thread


class ProcessSession:
    def __init__(self, config, model, tokenizer, max_input_length, init_token_idx, eos_token_idx, device, text):
        self.config = config
        self.model = model
        self.tokenizer = tokenizer
        self.max_input_length = max_input_length
        self.init_token_idx = init_token_idx
        self.eos_token_idx = eos_token_idx
        self.device = device
        self.text = text

        # inference
        self.worker = Thread(target=self.predict_sentiment, daemon=True)
        self.output = None

    def start(self):
        self.worker.start()

    def join(self):
        self.worker.join()

    def predict_sentiment(self):
        if self.model is not None:
            self.model.eval()
            tokens = self.tokenizer.tokenize(self.text)
            tokens = tokens[:self.max_input_length - 2]
            indexed = [self.init_token_idx] + self.tokenizer.convert_tokens_to_ids(tokens) + [self.eos_token_idx]
            tensor = torch.LongTensor(indexed).to(self.device)
            tensor = tensor.unsqueeze(0)
            prediction = torch.sigmoid(self.model(tensor))

            if prediction.item() >= self.config.threshold:
                self.output = {"positive": True, "score": prediction.item()}
            else:
                self.output = {"positive": False, "score": prediction.item()}
        else:
            self.output = {}
