from twitchio.ext import commands
import json

# load config file 
with open('config.json') as f:
    config = json.load(f)

token = config['access_token']
prefix = config['prefix']
initial_channels = config['initial_channels']


class Bot(commands.Bot):

    def __init__(self):
        # Initialise bot with access token, prefix and a list of channels to join
        super().__init__(
            token=token, 
            prefix=prefix,
            initial_channels=initial_channels
        )

    async def event_ready(self):
        # Notify when everything is ready
        # logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        # ignore messages from ourselves (bot)
        if message.echo:
            return

        # bot can read and respond to every message, even without prefix 
        # If the message is "ping" we want to send a message back with "pong!"
        # if message.content == 'ping':
        #     await message.channel.send('pong!')

        # print: timestamp (UTC datetime object), username, message content
        print(str(message.timestamp) + ': ' + message.author.name + ': ' + message.content)

        # append save chat message from first channel to csv file
        with open(initial_channels[0] + '.csv', 'a', encoding='utf-8') as file:
            file.write(str(message.timestamp) + ', ' + message.author.name + ', ' + message.content + '\n')

        # To use commands, we need to override the event_message method
        # We must let the bot know we want to handle and invoke our commands...
        #await self.handle_commands(message)

    # Commands use a different decorator...
    # Those will work with the prefix e.g. !hello
    @commands.command(name='hello')
    async def my_command(self, ctx):
        # ctx is the context object passed to our command...
        # ctx contains the message object, channel, author, guild, etc...
        # We can use this to send messages to the user...
        await ctx.send(f'Hello {ctx.author.name}!')

    # ping command, if our prefix is !, this will be called with !ping...
    @commands.command(name='ping')
    async def ping_command(self, ctx):
        await ctx.send(f'Pong!')


bot = Bot()
bot.run()