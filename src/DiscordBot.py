import discord
import asyncio
import personality_state
import threading
import ChatDatabase
import llamaAPI
import concurrent.futures

class AlpacaBot(discord.Client):

    ## initialize
    def __init__(self, AI_name = 'A', intents = None):
        super().__init__(intents)
        # set token
        self.token = token
        # set mutex
        self._pool = concurrent.futures.ThreadPoolExecutor()
        self.lock = threading.Lock()
        # set AI name and default prompt
        self.AI_name = AI_name
        self.user_name = 'Q'
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
    intents = discord.Intents.default()
    intents.message_content = True

    client = AlpacaBot(AI_name = 'A', intents=intents)
    client.run(token)