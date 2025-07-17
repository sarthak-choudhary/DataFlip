import vertexai
from vertexai.generative_models import (
    GenerativeModel, 
    SafetySetting, 
    HarmCategory, 
    HarmBlockThreshold,
    Content,
    Part
)
from .Model import Model
from anthropic import AnthropicVertex

class Vertex(Model):
    def __init__(self, config):
        super().__init__(config)
        self.project = config["api_key_info"]["project"]
        self.location = config["api_key_info"]["location"]
        self.model_name = config["model_info"]["name"]
        self.client = vertexai.init(project=self.project, location=self.location)

        self.max_output_tokens = int(config["params"]["max_output_tokens"])
        self.thinking_budget = int(config["params"]["max_thinking_tokens"])
        
    def query(self, msg):
        text_split = msg.split('\nText: ')
        assert (len(text_split) == 2)

        model = GenerativeModel(
            self.model_name,
            system_instruction=text_split[0],
        )
        response = model.generate_content(
            contents=[
                Content(
                    role="user",
                    parts=[Part.from_text("\nText: " + text_split[1])]
                ),
            ],
            safety_settings=[
                SafetySetting(
                    category=HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                    threshold=HarmBlockThreshold.BLOCK_NONE
                ),
                SafetySetting(
                    category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                    threshold=HarmBlockThreshold.BLOCK_NONE
                ),
                SafetySetting(
                    category=HarmCategory.HARM_CATEGORY_HARASSMENT,
                    threshold=HarmBlockThreshold.BLOCK_NONE
                ),
                SafetySetting(
                    category=HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                    threshold=HarmBlockThreshold.BLOCK_NONE
                ),
            ],
            generation_config={
                "max_output_tokens": self.max_output_tokens,
                **{
                    "thinking_config": {
                        "thinking_budget": self.thinking_budget,
                    } if self.thinking_budget is not None else {}
                }
            },
        )
        return response.text            

class VertexAnthropic(Model):
    def __init__(self, config):
        super().__init__(config)
        self.project = config["api_key_info"]["project"]
        self.location = config["api_key_info"]["location"]
        self.model_name = config["model_info"]["name"]
        self.client = AnthropicVertex(project_id=self.project, region=self.location)

        self.max_output_tokens = int(config["params"]["max_output_tokens"])
        
    def query(self, msg):
        text_split = msg.split('\nText: ')
        assert (len(text_split) == 2)
        
        response = self.client.messages.create(
            messages=[{
                "role": "user",
                "content": "\nText: " + text_split[1],
            }],
            model=self.model_name,
            max_tokens=self.max_output_tokens,
            system=text_split[0],
        )
        return "\n".join(t.text for t in response.content)