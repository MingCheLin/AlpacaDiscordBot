import asyncio
import threading
import discord
import personality_state
import ChatDatabase
import llamaAPI

class AlpacaBot(discord.Client):
    '''
    Alapca discord bot class,
    used to set the discord bot and connect to Alpaca model and chat history database
    '''
    ## initialize
    def __init__(self, AI_name = 'A', user_name = 'Q', intents = None, sem_num = 1, model_path = "./src/models/model.bin"):
        super().__init__(intents=intents)
        # set semaphore
        self.sem = asyncio.Semaphore(sem_num)
        # set AI name and default prompt
        self.AI_name = AI_name
        self.user_name = user_name
        personality = personality_state.personality(self.AI_name, self.user_name)
        self.personality = personality.set_personality()
        # set alpaca model
        self.Alpaca = llamaAPI.Alpaca(model_path = model_path)


    ## bot login
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    ## Process after message receive
    async def on_message(self, message):
        # prevent self reply
        if message.author.id == self.user.id:
            return
        # check if the message syntex
        if not message.content.startswith(f"{self.user_name}: "):
            return
        # reset the chat history
        if message.content == f"{self.user_name}: reset":
            ChatDatabase.reset(message.channel.id)
            await message.channel.send("reset done!")
            return
        # provide guidance
        if message.content == f"{self.user_name}: help":
            await message.channel.send(f"- {self.user_name}:                       comunicate with bot\n- {self.user_name}: reset               clear chat history")
            return
        # do alpaca model eval
        asyncio.to_thread(self.Alpaca_eval(message))
        return
    
    ## Alpaca model eval
    async def Alpaca_eval(self, message):
        # use mutex to prevent cpu overload
        async with self.sem:
        # loading chat history and set AI personality
            prompt = ChatDatabase.load_chat_history(message.channel.id)
            if not prompt:
                prompt = self.personality
            user_message = prompt+ "\n" + message.content + "\n" + f"{self.AI_name}: "
            # eval
            res = await asyncio.to_thread(self.Alpaca.eval(user_message, self.AI_name, self.user_name))
            # reply to channel
            await message.channel.send(res)
            # update chat history
            ChatDatabase.update_chat_history(message.channel.id, user_message + res)
        return
    
if __name__ == "__main__":
    # load token and names
    file = open('./token.txt', 'r', encoding='UTF-8')
    data = list()
    with file as f:
        for line in f.read().splitlines():
            s = line.split(' ')
            data.append(s[1])
    f.close()
    token = data[0]
    if len(token) < 18:
        raise ValueError("token unvalid")
    AI_name = data[1] if data[1] else 'A'
    user_name = data[2] if data[2] else 'Q'
    model_path = data[3] 
    if not model_path:
        raise ValueError("model path unvalid")
    # set bot permission
    intents_test = discord.Intents.default()
    intents_test.message_content = True
    # run the bot
    client = AlpacaBot(AI_name = AI_name, user_name = user_name, intents = intents_test, model_path = model_path)
    client.run(token)
