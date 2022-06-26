import discord
import time
from gtts import gTTS
from discord import FFmpegPCMAudio

TOKEN = 'insert key in quotes'

client = discord.Client()

t = 15
t2 = 13

end_of_presentation = 'Time is up, thank you for presenting, any questions on what was shown?'
end_of_qaa = 'Time is up, thank you for the presentation'

eop_audio = gTTS(text=end_of_presentation, lang='en', slow=False)
eoqaa_audio = gTTS(text=end_of_qaa, lang='en', slow=False)

eop_audio.save("eop_audioclip.mp3")
eoqaa_audio.save("eoqaa_audioclip.mp3")

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

    if message.channel.name == 'timer':

        if user_message.startswith('!timer-start :'):

            user_voice = message.author.voice

            if user_voice is None:
                await message.channel.send(f'User is not in Voice Channel')
                return
            else:

                def countdown(t):
                    while t:
                        mins, secs = divmod(t, 60)
                        timer = '{:02d}:{:02d}'.format(mins, secs)
                        print(timer)
                        time.sleep(1)
                        t -= 1
                countdown(t)

                await message.channel.send(f'time\'s up {(user_message.split(":", 1)[1])}, Q & A time')
                voice_channel = message.author.voice.channel
                announcer = await voice_channel.connect()
                audio_source = FFmpegPCMAudio('eop_audioclip.mp3')
                announcer.play(audio_source)
                if announcer.isplaying():
                    return
                else:
                    await announcer.disconnect()

                    def countdown(t2):
                        while t2:
                            mins, secs = divmod(t2, 60)
                            timer = '{:02d}:{:02d}'.format(mins, secs)
                            print(timer)
                            time.sleep(1)
                            t2 -= 1
                    countdown(t2)

                    await message.channel.send(f'time\'s up {(user_message.split(":", 1)[1])}, thank you for your presentation')
                    voice_channel = message.author.voice.channel
                    #announcer = await voice_channel.connect()
                    #await announcer.disconnect()
                    return

client.run(TOKEN)
