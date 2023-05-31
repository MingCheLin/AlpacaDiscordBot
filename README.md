# AlpacaDiscordBot
This is a discord bot project that use Alpaca LLM to generate response to discord user. The main purpose is to provide a free, low hardware requirements discord client structure to everyone who want to host a GPT-like discord bot themselves. In this project, ![llama.cpp](https://github.com/ggerganov/llama.cpp#instruction-mode-with-alpaca), ![llama-cpp-python](https://github.com/abetlen/llama-cpp-python) and ![discord.py](https://discordpy.readthedocs.io/en/stable/) are used.
And for chinese user, ![Chinese-LLaMA-Alpaca](https://github.com/ymcui/Chinese-LLaMA-Alpaca) can be used to generate chinese Alpaca model.
對於中文使用者，![Chinese-LLaMA-Alpaca](https://github.com/ymcui/Chinese-LLaMA-Alpaca)可以用來將Alpaca模組藉由預訓練將其中文化。

## Alpaca 
Alpaca is a LLM(large language model) that fine-tuned from the LLaMA 7B model by ![Stanford Center for Research on Foundation Models](https://crfm.stanford.edu/2023/03/13/alpaca.html).

## Usage
### 1. Install discord.py and llama-cpp-python
``pip install llama-cpp-python discord.py``
### 2. Get alpaca model
For english user, please download the alpaca model from ![Hugging face](https://huggingface.co/models?other=alpaca) and follow ![llama.cpp](https://github.com/ggerganov/llama.cpp#instruction-mode-with-alpaca) to quantize the model.
中文使用者可以使用![Chinese-LLaMA-Alpaca](https://github.com/ymcui/Chinese-LLaMA-Alpaca)來得到中文預訓練模型並將其量化為4 bits。
And put the model into ``./src/models/ `` 
### 3. Create discord bot
Follow ![Create discord bot](https://discordpy.readthedocs.io/en/stable/discord.html) to create discord bot, and copy the token.
### 4. Set bot name, the user name, model path and discord bot token
the txt file ```token.txt``` looks like:
```
token: PUT_YOUR_TOKEN_HERE
AI_name: PUT_YOUR_AI_NAME_HERE
user_name: PUT_YOUR_USER_NAME_HERE
model_path: MODEL_PATH
```
``token`` : Discord bot token
``AI_name`` : Default is ``A`` if make this parameteer empty. In addition, use ``Miku`` or ``AI_assistance`` will certain personality.
``user_name`` : Default is ``Q`` if make this parameteer empty, this would be the command prefix, type ``{AI_name}: `` with the user input to communicate with bot, e.g. if set ``AI_name`` as 'Alpaca', enter ``Alpaca: Hello!`` could say hello to the bot.
``model_path`` : The model path, e.g.:``./src/models/ggml-model-q4_0.bin `` 
### 5. Run bot
enter:
``python DiscordBot.py`` 
to run the bot.


## Roadmap
1. Fix the discord api warning ``WARNING  discord.gateway Shard ID None heartbeat blocked for more than XX seconds.``
2. Tune the alpaca model parameter.
3. Make another multiprocess structure to handle multichannel request.
4. etc...
