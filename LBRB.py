import discord
from translate import Translator
from langdetect import detect

TOKEN = 'insert key in quotes'

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f'{username}: {user_message} ({channel})')

    if message.author == client.user:
        return

    if message.channel.name == 'general-multlang':
        lang = (detect(user_message))
        if lang != 'en':
            print(f'Language: ', lang)
            translator = Translator(to_lang = 'en', from_lang= lang)
            translation = translator.translate(message.content)
            print(f'Translation: ', translation)
            if user_message != translation:
                await message.reply(translation)
                return

client.run(TOKEN)
