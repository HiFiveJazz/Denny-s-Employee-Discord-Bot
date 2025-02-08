import discord

class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
    
    async def on_voice_state_update(self, member, before, after):
        guild = member.guild

        # Get all voice channels sorted by position
        voice_channels = sorted(guild.voice_channels, key=lambda ch: ch.position)
        voice_channel_names = {channel.name for channel in voice_channels}

        if after.channel:
            user_count = len(after.channel.members)
            print(f"{member} joined {after.channel.name}.")
            print(f"Users in {after.channel.name}: {user_count}")

            # Dynamically name the next channel based on existing ones
            base_name = after.channel.name.split(" ")[0]
            similar_channels = [ch for ch in voice_channels if ch.name.startswith(base_name)]
            new_channel_name = f"{base_name} {len(similar_channels) + 1}"

            # Ensure the new channel doesn't already exist
            if new_channel_name not in voice_channel_names:
                print(f"Creating an empty channel: {new_channel_name} below {after.channel.name}...")

                new_channel = await guild.create_voice_channel(
                    new_channel_name, 
                    category=after.channel.category, 
                    position=after.channel.position + 1
                )
                print(f"New voice channel created: {new_channel.name}")

        # User left a voice channel
        if before.channel and after.channel != before.channel:
            user_count = len(before.channel.members)
            print(f"{member} left {before.channel.name}.")
            print(f"Users in {before.channel.name}: {user_count}")

            # Check the deletion rule for all channels except "general"
            for index, channel in enumerate(voice_channels):
                if channel.name == "general":
                    continue  # Skip the main general channel

                if len(channel.members) == 0:  # If this channel is empty
                    # Find the channel above it
                    if index > 0:
                        above_channel = voice_channels[index - 1]
                        if above_channel.name != "general" and len(above_channel.members) == 0:
                            print(f"Both {channel.name} and {above_channel.name} are empty. Deleting {channel.name}...")
                            await channel.delete()
                            print(f"{channel.name} has been deleted.")

    async def on_member_join(self, member):
        """Logs when a new member joins the server."""
        print(f"New member joined: {member.name}#{member.discriminator} (ID: {member.id})")

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True  # Enable voice state intents
intents.members = True  # Enable member events (on_member_join)

client = Client(intents=intents)

# Replace 'API_KEY' with your actual API key
with open("API_KEY.txt", "r") as file:
    API_KEY = file.read().strip()

client.run(API_KEY)

