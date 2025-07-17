import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel

from .Model import Model


class Huggingface(Model):
    def __init__(self, config):
        super().__init__(config)
        self.max_output_tokens = int(config["params"]["max_output_tokens"]) 
        self.device = config["params"]["device"]

        self.base_model_id = config["model_info"]['name']

        self.bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16
        )

        self.model = AutoModelForCausalLM.from_pretrained(self.base_model_id, quantization_config=self.bnb_config, device_map="auto")
        self.model.eval()
        
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.base_model_id,
            padding_side="left",
            add_eos_token=True,
            add_bos_token=True,
            device_map="auto"
        )
        
        self.tokenizer.pad_token = self.tokenizer.eos_token
            
    def print_model_info(self):
        print(f"{'-'*len(f'| Model name: {self.name}')}\n| Provider: {self.provider}\n| Model name: {self.name}\n| FT Path: {self.ft_path}\n{'-'*len(f'| Model name: {self.name}')}")
    
    def query(self, msg):
        text_split = msg.split('\nText: ')
        assert len(text_split) == 2
        
        processed_eval_prompt = self.tokenizer.apply_chat_template([
            {"role": "system", "content": text_split[0]},
            {"role": "user", "content": "\nText: " + text_split[1]}
        ], tokenize=False)
        
        input_ids = self.tokenizer(processed_eval_prompt, return_tensors="pt").to("cuda")
        
        self.model.eval()
        with torch.no_grad():
            output = self.tokenizer.decode(
                self.model.generate(
                    **input_ids, 
                    max_new_tokens=self.max_output_tokens, 
                    repetition_penalty=1.2
                )[0, input_ids["input_ids"].shape[1]-1:], 
                skip_special_tokens=True
            ).lstrip("assistant\n\n")
        return output