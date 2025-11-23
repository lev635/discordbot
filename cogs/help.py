import os
from dotenv import load_dotenv

import discord
from discord import app_commands
from discord.ext import commands

load_dotenv()

ARCHIVE_EMOJI = os.environ['ARCHIVE_EMOJI']
ARCHIVE_CRITERION = int(os.environ['ARCHIVE_CRITERION'])

class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="help",
        description="使い方"
    )
    async def help(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.defer()
        message = """## コマンド
- `/help` : これを表示
- `/tf (絵文字の名前)` : 絵文字をファイルにして送信
- `/archive (メッセージのURL)` : 指定されたメッセージを保存
## 機能
- メッセージのリンクを貼ると、内容を展開します
- `:{ARCHIVE_EMOJI}:` が {ARCHIVE_CRITERION} 個以上ついたメッセージを保存します
""".format(
            ARCHIVE_EMOJI=ARCHIVE_EMOJI,
            ARCHIVE_CRITERION=ARCHIVE_CRITERION
        )
        await interaction.followup.send(message)

async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))
