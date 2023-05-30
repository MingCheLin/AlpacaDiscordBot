from multiprocessing import cpu_count 
from llama_cpp import Llama

class Alpaca():

    def __init__(self, 
                 model_name = "./drive/MyDrive/ggml-model-q4_0.bin", 
                 n_ctx = 512,
                 max_tokens = 128,
                 n_threads = None,
                ):
        model_path = model_name
        if not n_threads:
            n_threads = max(cpu_count()//2, 1)
        self.n_ctx = n_ctx
        self.max_tokens = max_tokens
        self.alpaca = Llama(model_path=model_path, n_ctx = self.n_ctx, n_threads=n_threads)

    def eval(self, prompt, character, user):
        prompt = self.check_prompt_size(prompt, character)
        output = self.alpaca(prompt, max_tokens=self.max_tokens, stop=[f"{user}:"])
        return output['choices'][0]['text']

    def check_prompt_size(self, prompt, character):
        prompt_tokens = self.alpaca.tokenize(b" " + prompt.encode("utf-8"))
        if len(prompt_tokens) + self.max_tokens > self.n_ctx:
            return f"{character}:" + prompt[len(prompt)//2:].split(f"{character}:", 1)[1]
        return prompt
    