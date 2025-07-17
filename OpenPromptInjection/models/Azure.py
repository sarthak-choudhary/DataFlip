from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from .Model import Model

class Azure(Model):
    def __init__(self, config):
        super().__init__(config)
        self.endpoint = config["api_key_info"]["endpoint"]
        self.api_key = config["api_key_info"]["api_keys"][config["api_key_info"]["api_key_use"]]
        self.model_name = config["model_info"]["name"]
        self.api_version = config["api_key_info"]['api_version'] 
        self.max_output_tokens = int(config["params"]["max_output_tokens"])
        
        self.client = ChatCompletionsClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.api_key),
            api_version=self.api_version,
        )
        
    def query(self, msg, thinking=False):
        text_split = msg.split('\nText: ')
        assert (len(text_split) == 2)

        response = self.client.complete(
            messages=[
                SystemMessage(content=text_split[0]),
                UserMessage(content="\nText: " + text_split[1]),
            ],
            model=self.model_name,
            max_tokens=self.max_output_tokens,
        )
        content = response.choices[0].message.content   

        if not thinking and "</think>" in content:
            return content.split("</think>")[1]

        return content