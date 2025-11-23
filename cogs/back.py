import os
import re
import datetime
from dotenv import load_dotenv

import discord
from discord.ext import commands

load_dotenv()

TOKEN = os.environ['TOKEN']
MAXIMUM_LENGTH = 1950

ARCHIVE_CHANNEL = int(os.environ['ARCHIVE_CHANNEL'])

TEMP_CHANNEL = int(os.environ['TEMP_CHANNEL'])

ARCHIVE_CRITERION = int(os.environ['ARCHIVE_CRITERION'])

COLOR_EMBED = int(os.environ['COLOR_EMBED'], 0)
COLOR_ARCHIVE = int(os.environ['COLOR_ARCHIVE'], 0)

ARCHIVE_EMOJI = os.environ['ARCHIVE_EMOJI']

URL_REGEX = r"https://discord.com/channels/(?P<guild>[0-9]{17,20})/(?P<channel>[0-9]{17,20})/(?P<message>[0-9]{17,20})"


class Back(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Embed
    async def dispander(self, message) -> None:
        messages = []
        for idx in re.finditer(URL_REGEX, message.content):
            if message.guild.id != int(idx["guild"]):
                continue
            try:
                ms = await self.bot.get_channel(int(idx["channel"])).fetch_message(int(idx["message"]))
                messages.append(ms)
            except:
                pass
        for ms in messages:
            embed = await self.make_embed(ms, COLOR_EMBED)
            await message.channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        # Embed
        await self.dispander(message)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, event):
        ch = self.bot.get_channel(event.channel_id)
        ms = await ch.fetch_message(event.message_id)

        for re in ms.reactions:
            em = re.emoji
            st = ''
            try:
                st = em.name
            except:
                pass
            if st == ARCHIVE_EMOJI:
                users = [user async for user in re.users()]
                if len(users) == ARCHIVE_CRITERION:
                    embed = await self.make_embed(ms, COLOR_ARCHIVE)
                    ch = self.bot.get_channel(ARCHIVE_CHANNEL)
                    if await self.check_embed(ch, ms):
                        await ch.send(embed=embed)
                        
    async def make_embed(self, message, color_code):
        embed = discord.Embed(
            color=color_code, description=message.clean_content)
        embed.set_author(name=message.author.display_name,
                            icon_url=message.author.display_avatar.url, url=message.jump_url)
        time = (message.created_at + datetime.timedelta(hours=9)
                ).strftime("%Y/%m/%d %H:%M")
        name = message.channel.name
        embed.set_footer(text=f"{name} {time} {message.id}")
        for attachment in message.attachments:
            f = await attachment.to_file(filename="image.png")
            tmpmsg = await self.bot.get_channel(TEMP_CHANNEL).send(file=f)
            embed.set_image(url=tmpmsg.attachments[0].proxy_url)
        return embed

    async def check_embed(self, channel, message):
        ok = True
        async for msg in channel.history(limit=MAXIMUM_LENGTH//10):
            vec = msg.embeds
            for emb in vec:
                if emb == None:
                    continue
                s = emb.footer.text
                if s == None:
                    continue
                v = s.split("   ")
                if len(v) != 3:
                    continue
                if str(message.id) == v[2]:
                    ok = False
        return ok

async def setup(bot: commands.Bot):
    await bot.add_cog(Back(bot))