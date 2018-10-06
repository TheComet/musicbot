import discord
import random
import asyncio
import pickle
import random
from urllib.parse import urlparse, parse_qs, urlencode

TEXT_CHANNEL_ID = "498086947105931276"
VOICE_CHANNEL_ID = "498086947105931278"
# TOKEN = "NDk3ODY3MzAzODM3MzY4MzM5.DplrfA.mL1m2lO_zmnAQ2pomM36GIEjrdk"
TOKEN = "NDk4MDg2Mjk4MjQ2OTcxNDE0.Dpom3A.JDbPuFTPomA8IR_xBCE-Yu8TClI"

class TheBot(object):
    def __init__(self):
        self.client = discord.Client()

        self.voice_channel = None
        self.is_playing = False
        self.player = None
        self.music_queue = pickle.load(open('music_list.txt', 'rb'))

        async def action_skip(message):
            self.player.stop()

        async def action_gay(message):
            self.music_queue.insert(1, self.music_queue[-1])
            self.music_queue.pop(-1)
            self.player.stop()
            await self.client.send_message(message.channel, "bar")

        async def action_pause(message):
            self.player.pause()
            await self.client.send_message(message.channel, "paws")

        async def action_resume(message):
            await self.client.send_message(message.channel, "résumé")
            self.player.resume()

        async def action_shuffle(message):
            first, self.music_queue = self.music_queue[0:]
            random.shuffle(self.music_queue)
            self.music_queue.insert(0, first)
            await self.client.send_message(message.channel, "Playlist was shuffled.")

        async def action_list(message):
            if len(message.content.split(" ")) > 1 and message.content.split(" ")[1] == "pv":
                await self.client.send_message(message.channel, "{}".format(self.music_queue))
            else:
                await self.client.send_message(message.channel, "<"+">\n<".join(self.music_queue)+">")

        async def action_help(message):
            await self.client.send_message(message.channel,
                                           "```Command list:\n" +
                                           "\n".join(
                                               [k.ljust(4+max(map(len, self.actions.keys()))) +
                                                self.actions[k][1]
                                                for k in self.actions.keys()])
                                           + "```")

        self.actions = {
            ".pause":   (action_pause,   "pause track"),
            ".resume":  (action_resume,  "resume track"),
            ".skip":    (action_skip,    "skip track"),
            ".shuffle": (action_shuffle, "shuffle playlist"),
            ".gay":     (action_gay,     "???"),
            ".list":    (action_list,    "[pv] list queued urls, optional preview"),
            ".help":    (action_help,    "print this help"),
        }

        @self.client.event
        async def on_ready():
            print('Logged in as')
            print(self.client.user.name)
            print(self.client.user.id)
            print('------')

            vc = self.client.get_channel(VOICE_CHANNEL_ID)
            self.voice_channel = await self.client.join_voice_channel(vc)
            asyncio.ensure_future(self.player_task())

            await self.client.send_message(self.client.get_channel(TEXT_CHANNEL_ID), "OwO I'm back OwO")

        @self.client.event
        async def on_message(message):
            try:
                if message.author.bot:
                    return ()

                if message.content[0] == ".":
                    await self.actions[message.content.split(" ")[0]][0](message)
                    return()

                for msg_cont in message.content.split('\n'):
                    try:
                        url = "https://www.youtube.com/watch/?" + urlencode(dict(v=parse_qs(urlparse(msg_cont).query)['v'][0]))
                    except:
                        continue
                    self.add_to_queue(url)
                    await self.client.send_message(message.channel, "Added to queue (position {})".format(len(self.music_queue)-1))
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
                    if len(self.music_queue) > 0:
                        self.music_queue.pop(0)
                    pickle.dump(self.music_queue, open('music_list.txt', 'wb'))

            next_url = self.music_queue[0]
            self.player = await self.voice_channel.create_ytdl_player(next_url)
            self.player.start()
            await self.client.send_message(self.client.get_channel(TEXT_CHANNEL_ID),
                                           "Playing {} ({})\n{} left in queue".format(
                                               self.player.title,
                                               self.player.duration,
                                               len(self.music_queue) - 1))


bot = TheBot()
bot.client.run(TOKEN)
