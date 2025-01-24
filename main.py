import discord

class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
    
    async def on_voice_state_update(self, member, before, after):
        # Check if the user joined a voice channel
        if after.channel:
            guild = after.channel.guild
            
            # Get all voice channels in the guild
            voice_channels = [channel for channel in guild.voice_channels]
            print(f"{voice_channels}")
            
            # Check if the user joined the only voice channel on the server
            if len(voice_channels) == 1 and after.channel == voice_channels[0]:
                existing_channel = voice_channels[0]
                print(f"{member} joined {existing_channel.name}. Creating a new voice channel...")

                # Create a new voice channel under the same category
                new_channel_name = f"{existing_channel.name} Clone"
                new_channel = await guild.create_voice_channel(
                    new_channel_name, 
                    category=existing_channel.category  # Place it in the same category
                )
                print(f"New voice channel created: {new_channel.name}")

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True  # Enable voice state intents

client = Client(intents=intents)

# Replace 'API_KEY' with your actual API key
with open("API_KEY.txt", "r") as file:
    API_KEY = file.read().strip()

client.run(API_KEY)

