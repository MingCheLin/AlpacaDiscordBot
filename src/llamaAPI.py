from multiprocessing import cpu_count 
from typing import List,Optional
from llama_cpp import Llama

class Alpaca():

    def __init__(self, 
                 model_path: str = "./drive/MyDrive/ggml-model-q4_0.bin", 
                 n_ctx: int = 512,
                 n_parts: int = -1,
                 n_gpu_layers: int = 0,
                 seed: int = 1337,
                 f16_kv: bool = True,
                 logits_all: bool = False,
                 vocab_only: bool = False,
                 use_mmap: bool = True,
                 use_mlock: bool = False,
                 embedding: bool = False,
                 n_threads: Optional[int] = None,
                 n_batch: int = 512,
                 last_n_tokens_size: int = 64,
                 lora_base: Optional[str] = None,
                 lora_path: Optional[str] = None,
                 verbose: bool = True,
                ):
        '''
        Model initialization, including all model parameters, most important are: 
        model_path  : Model path.
        n_ctx       : Maximum context size.
        n_threads   : Number of threads to use. If None, the number of threads is automatically determined. 
        '''
        self.model_path = model_path
        if not n_threads:
            n_threads = max(cpu_count()//2, 1)
        self.n_ctx = n_ctx
        self.alpaca = Llama(model_path=self.model_path, 
                            n_ctx = self.n_ctx, 
                            n_threads=n_threads,
                            n_parts = n_parts,
                            n_gpu_layers = n_gpu_layers,
                            seed = seed,
                            f16_kv = f16_kv,
                            logits_all = logits_all,
                            vocab_only = vocab_only,
                            use_mmap = use_mmap,
                            use_mlock = use_mlock,
                            embedding = embedding,
                            n_batch = n_batch,
                            last_n_tokens_size = last_n_tokens_size,
                            lora_base = lora_base,
                            lora_path = lora_path,
                            verbose = verbose,
                            )
    def eval(self, 
             prompt: str, 
             character: str, 
             user: str,
             usersuffix: Optional[str] = None,
             max_tokens: int = 128,
             temperature: float = 0.8,
             top_p: float = 0.95,
             logprobs: Optional[int] = None,
             echo: bool = False,
             frequency_penalty: float = 0.0,
             presence_penalty: float = 0.0,
             repeat_penalty: float = 1.1,
             top_k: int = 40,
             stream: bool = False,
             tfs_z: float = 1.0,
             mirostat_mode: int = 0,
             mirostat_tau: float = 5.0,
             mirostat_eta: float = 0.1,
             model: Optional[str] = None,
             stopping_criteria: Optional[List] = None,
             logits_processor: Optional[List] = None,
             ):
        '''
        Evalute the response to user input,
        prompt      :   The user input.
        character   :   The AI's name.
        user        :   User name.
        '''
        prompt = self.check_prompt_size(prompt, character, max_tokens)
        if not user:
            stop = []
        else:
            stop = [f"{user}:"]
        output = self.alpaca(prompt, 
                             max_tokens=max_tokens, 
                             stop = stop,
                             usersuffix = usersuffix,
                             temperature = temperature,
                             top_p = top_p,
                             logprobs = logprobs,
                             echo = echo,
                             frequency_penalty = frequency_penalty,
                             presence_penalty = presence_penalty,
                             repeat_penalty = repeat_penalty,
                             top_k = top_k,
                             stream = stream,
                             tfs_z = tfs_z,
                             mirostat_mode = mirostat_mode,
                             mirostat_tau = mirostat_tau,
                             mirostat_eta = mirostat_eta,
                             model = model,
                             stopping_criteria = stopping_criteria,
                             logits_processor = logits_processor,
                             )
        return output['choices'][0]['text']

    def check_prompt_size(self, prompt, character, max_tokens):
        '''
        Prevent the user's input exceed the maximum context size'''
        prompt_tokens = self.alpaca.tokenize(b" " + prompt.encode("utf-8"))
        if len(prompt_tokens) + max_tokens > self.n_ctx:
            return f"{character}:" + prompt[len(prompt)//2:].split(f"{character}:", 1)[1]
        return prompt

if __name__ == "__main__":
    print("testing...")
    alpaca = Alpaca(model_path="./src/models/ggml-model-q4_0.bin")
    prompt_test = input()
    res = alpaca.eval(f"Q: {prompt_test} A: ", 'A', 'Q')
    print(res)