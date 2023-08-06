"""Client example for sending 'hello world' as direct message"""
from discordproxy.client import DiscordClient

client = DiscordClient()
client.create_direct_message(user_id=152878250039705600, content="Hello, world!")
