import discord
import asyncio
import personality_state
import threading
import ChatDatabase
import llamaAPI
import concurrent.futures

class AlpacaBot(discord.Client):
    '''
    Alapca discord bot class,
    used to set the discord bot and connect to Alpaca model and chat history database
    '''
    ## initialize
    def __init__(self, AI_name = 'A', user_name = 'Q', intents = None):
        super().__init__(intents)
        # set mutex
        self._pool = concurrent.futures.ThreadPoolExecutor()
        self.lock = threading.Lock()
        # set AI name and default prompt
        self.AI_name = AI_name
        self.user_name = user_name
        personality = personality_state.personality(self.AI_name, self.user_name)
        self.personality = personality.set_personality()
        # set alpaca model
        self.Alpaca = llamaAPI.Alpaca()


    ## bot login
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, message):
        # prevent self reply
        if message.author.id == self.user.id:
            return
        # check if the message syntex
        if not message.content.startswith(f"{self.user_name}: "):
            return
        if message.content == f"{self.user_name}: reset":
            ChatDatabase.reset(message.channel)
        # loading chat history and set AI personality
        prompt = ChatDatabase.load_chat_history(message.channel)
        if not prompt:
            prompt = self.personality
        user_message = prompt + message.content + f"{self.AI_name}: "
        # use mutex to prevent cpu overload
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(self._pool, self.lock.acquire)
        res = self.Alpaca.eval(user_message, self.AI_name, self.user_name)
        self.lock.release()
        # reply to channel
        await message.channel.send(res)
        # update chat history
        ChatDatabase.update_chat_history(message.channel, user_message + res)


if __name__ == "__main__":
    # load token and names
    file = open('./token.txt', 'r', encoding='UTF-8')
    data = list()
    with file as f:
        for line in f.read().splitlines():
            s = line.split(' ')
            data.append(s)
    f.close()
    token = data[0]
    if len(token) < 18:
        raise ValueError("token unvalid")
    AI_name = data[1] if data[1] else 'A'
    user_name = data[2] if data[2] else 'Q'
    # set bot permission
    intents_test = discord.Intents.default()
    intents_test.message_content = True
    # run the bot
    client = AlpacaBot(AI_name = AI_name, user_name = user_name, intents = intents_test)
    client.run(token)
