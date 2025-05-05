import discord
import google.genai as genai
from discord.ext import commands

import os
from os.path import join, dirname
from dotenv import load_dotenv

# botのクラス
class Idola(commands.Bot):
    def __init__(self):
        super().__init__(
            intents=intents,
            help_command=None,
            command_prefix='h!'
        )
        
        # Geminiの設定
        self.client = genai.Client(api_key=GOOGLE_API_KEY)
        self.guild = self.get_guild(GUILD_ID)
            
        # cogsを読み込む
        self.initial_extensions = [
            'cogs.summary',
            'cogs.explain',
            'cogs.review',
        ]
    
    async def setup_hook(self):
        for extension in self.initial_extensions:
            await self.load_extension(extension)
        await self.tree.sync(guild=self.guild)
        
    
    async def on_ready(self):
        print("get on ready!")


# .envファイルを読み込む
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# 環境変数を取得
GUILD_ID = int(os.getenv('GUILD_ID'))
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

intents = discord.Intents.default()
intents.message_content = True

bot = Idola()
bot.run(DISCORD_TOKEN)
