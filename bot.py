import discord
import asyncio
import pickle
from urllib.parse import urlparse, parse_qs, urlencode


class TheBot(object):
    def __init__(self):
        self.client = discord.Client()

        self.voice_channel = None
        self.is_playing = False
        self.player = None
        self.music_queue = pickle.load(open('music_list.txt', 'rb'))

        @self.client.event
        async def on_ready():
            print('Logged in as')
            print(self.client.user.name)
            print(self.client.user.id)
            print('------')

            vc = self.client.get_channel("497830999707746305")
            self.voice_channel = await self.client.join_voice_channel(vc)
            asyncio.ensure_future(self.player_task())

            await self.client.send_message(self.client.get_channel("497830999204560920"), "OwO I'm back OwO")

        @self.client.event
        async def on_message(message):
            try:
                if message.author.bot:
                    return ()

                if message.content == ".skip":
                    self.player.stop()
                    return ()
                if message.content == ".gay":
                    await self.client.send_message(message.channel, "bar")
                    return ()
                elif message.content == ".pause":
                    self.player.pause()
                    await self.client.send_message(message.channel, "paws")
                    return ()
                elif message.content == ".resume":
                    await self.client.send_message(message.channel, "résumé")
                    self.player.resume()
                    return ()
                elif message.content == ".help":
                    await self.client.send_message(message.channel, "```Command list:\n.skip\n.pause\n.resume\n.help```")
                    return ()

                for possible_url in message.content.split('\n'):
                    try:
                        url = "https://www.youtube.com/watch/?" + urlencode(dict(v=parse_qs(urlparse(possible_url).query)['v'][0]))
                    except:
                        continue

                    self.add_to_queue(url)
                    await self.client.send_message(message.channel, "Added to queue (position {})".format(len(self.music_queue)))
            except:
                await self.client.send_message(message.channel, "OwO OOPSIE WOOPSIE!! Uwu We made a fucky wucky!! A wittle fucko boingo! The code monkeys at our headquarters are working VEWY HAWD to fix this! OwO")

    def add_to_queue(self, url):
        self.music_queue.append(url)
        pickle.dump(self.music_queue, open('music_list.txt', 'wb'))

    async def player_task(self):
        while True:
            await asyncio.sleep(1)
            if len(self.music_queue) == 0:
                continue

            if self.player:
                if not self.player.is_done():
                    continue
                else:
                    self.music_queue.pop(0)
                    pickle.dump(self.music_queue, open('music_list.txt', 'wb'))

            next_url = self.music_queue[0]
            self.player = await self.voice_channel.create_ytdl_player(next_url)
            self.player.start()
            await self.client.send_message(self.client.get_channel("497830999204560920"), "Playing {} ({})\n{} left in queue".format(
                self.player.title, self.player.duration, len(self.music_queue) - 1))


bot = TheBot()
bot.client.run('NDk3ODY3MzAzODM3MzY4MzM5.DplrfA.mL1m2lO_zmnAQ2pomM36GIEjrdk')
