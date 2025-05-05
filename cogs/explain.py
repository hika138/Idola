import discord
from discord.ext import commands
from google import genai
from google.genai import types

# 解説を生成するCog
# 使い方: /explain <内容>
class Explain(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.client: genai.Client = bot.client
        self.google_search_tool = types.Tool(google_search = types.GoogleSearch())

    @discord.app_commands.command(
        name="explain",
        description="説明を生成します"
    )
    async def explain(self, ctx: discord.Interaction, content: str):
        # 解説を生成
        await ctx.response.defer()
        response = self.client.models.generate_content(
            model="gemini-2.5-flash-preview-04-17",
            contents=
            f"""
                /! から始まる行は会話ではなく命令です。必ず従い、次回以降の会話に反映してください。
                
                /! あなたはDiscordのbotです。
                /! あなたは解説を生成するAIです。
                /! 返答はせず、解説だけをしてください。
                
                /! フォーマットは以下の通りです。
                /! # 〇〇についての解説
                /! ## 概要
                /! ## 参考リンク
                
                /! 解説は日本語でしてください。
                /! 解説の正しさを保証するために検索を行い、必ず参考にした情報ソースのリンクを提示してください。
                /! 解説はリンクも含めて1500文字以内でしてください。
                /! 参考リンクはURLだけを提示してください。
                /! 参考リンク切れがないように送信前に確認してください。
                /! 参考リンクは最小で1件、最大で3件提示してください。
                /! 以下の内容について解説してください。
                {content}
            """,        
            config=types.GenerateContentConfig(
                tools=[self.google_search_tool],
                max_output_tokens=1000,
            ),
        )
        
        # メッセージを整形
        response_message = "AIによる解説\n" + response.text
        # 送信
        if len(response_message) > 2000:
            response_message = response_message[:2000] + "..."
        await ctx.followup.send(response_message)
        return
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Explain(bot))