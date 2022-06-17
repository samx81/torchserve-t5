import torch
import os
import logging
import json
from abc import ABC

from ts.torch_handler.base_handler import BaseHandler
from transformers import T5Tokenizer, T5ForConditionalGeneration
from transformers import T5TokenizerFast

logger = logging.getLogger(__name__)

class TransformersSeqGeneration(BaseHandler, ABC):
    def __init__(self):
        super().__init__()
        self.initialized = False
        self.device = None

    def initialize(self, ctx):
        self.manifest = ctx.manifest
        properties = ctx.system_properties
        model_dir = properties.get("model_dir")
        serialized_file = self.manifest["model"]["serializedFile"]
        model_pt_path = os.path.join(model_dir, serialized_file)
        self.device = torch.device(
            "cuda:" + str(properties.get("gpu_id"))
            if torch.cuda.is_available()
            else "cpu")
        print("DEVICE", self.device)
        # read configs for the mode, model_name, etc. from setup_config.json
        setup_config_path = os.path.join(model_dir, "setup_config.json")
        if os.path.isfile(setup_config_path):
            with open(setup_config_path) as setup_config_file:
                self.setup_config = json.load(setup_config_file)
        else:
            logger.warning("Missing the setup_config.json file.")
        # Loading the model and tokenizer from checkpoint and config files based on the user's choice of mode
        # further setup config can be added.
        self.tokenizer = T5TokenizerFast.from_pretrained(model_dir)
        if self.setup_config["save_mode"] == "torchscript":
            self.model = torch.jit.load(model_pt_path)
        elif self.setup_config["save_mode"] == "pretrained":
            self.model = T5ForConditionalGeneration.from_pretrained(model_dir)
        else:
            logger.warning("Missing the checkpoint or state_dict.")
        self.model.to(self.device)
        self.model.eval()
        logger.info(f"Transformer model from path {model_dir} loaded successfully")
        self.initialized = True

    def preprocess(self, requests):
        input_ids_batch = None
        attention_mask_batch = None
        for idx, data in enumerate(requests):
            data = data["body"]
            input_text = data["text"]
            inputs = self.tokenizer(input_text, max_length=60, return_tensors="pt",
                    pad_to_max_length=True, add_special_tokens=True)
            input_ids = inputs["input_ids"].to(self.device)
            attention_mask = inputs["attention_mask"].to(self.device)

            if input_ids.shape is not None:
                if input_ids_batch is None:
                    input_ids_batch = input_ids
                    attention_mask_batch = attention_mask
                else:
                    input_ids_batch = torch.cat((input_ids_batch, input_ids), 0)
                    attention_mask_batch = torch.cat((attention_mask_batch, attention_mask), 0)
        return input_ids_batch, attention_mask_batch

    def inference(self, input_batch):
        input_ids_batch, attention_mask_batch = input_batch
        marshalled_batch = input_ids_batch.to(self.device)
        with torch.no_grad():
            # print("NO GRAD")
            outputs = self.model.generate(marshalled_batch, max_length=60).cpu()
        return outputs

    def postprocess(self, outputs):
        inferences = []
        for i, x in enumerate(outputs):
            inferences.append(self.tokenizer.decode(outputs[i], skip_special_tokens=True))
        return inferences
