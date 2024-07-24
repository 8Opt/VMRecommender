from typing import Union
from transformers import pipeline

from vmrec.prompts import PROMPT_TEMPLATE

class TinyAgent: 
    def __init__(self, config): 
        self.config = config
        self.messages = [
            {"role": "system", 
             "content": "You are a chatbot that specializes in recommending appropriate virtual machine setting for client."}
        ]

    def query(self, input, context:Union[str, None]=None, is_text:bool=True):
        pipe = pipeline(task=self.config['task'], 
                        model=self.config['model_id'])
        if context is None: 
            context = "There is no additional information."
        input = PROMPT_TEMPLATE.format(question=input, 
                                        context=context)
        
        self.messages.append({"role": "user", 
                              "content": input})
        
        prompt = pipe.tokenizer.apply_chat_template(
            self.messages, tokenize=False, add_generation_prompt=True
        )

        outputs = pipe(prompt,
            **self.config['settings']
        )

        if is_text: 
            return outputs[0]['generated_text']

        return outputs