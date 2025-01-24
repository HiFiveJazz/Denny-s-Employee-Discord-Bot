import discord

with open("API_KEY.txt", "r") as file:
    API_KEY = file.read().strip()


class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

intents = discord.Intents.default()
intents.message_content = True


client = Client (intents=intents)
client.run(API_KEY)
