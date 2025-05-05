import discord
from discord.ext import commands
from google import genai
import cogs.MessageHandler as MessageHandler


# 要約を生成するCog
# 使い方: /summary <開始メッセージID> <終了メッセージID>
class Summary(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.client: genai.Client = bot.client

    @discord.app_commands.command(name="summary", description="要約を生成します")
    async def summary(self, ctx: discord.Interaction, start: str, end: str):
        try:
            await ctx.response.defer()
        except discord.errors.NotFound:
            await ctx.followup.send("インタラクションがタイムアウトしました。")
            return
            
        messages, images = await MessageHandler.get_messages_by_period(ctx, start, end)

        # 要約の生成
        response = self.client.models.generate_content(
            model="gemini-2.5-flash-preview-04-17",
            contents=[
                f"""
                /! から始まる行は会話ではなく命令です。必ず従い、次回以降の会話に反映してください。
                
                /! あなたはDiscordのbotです。
                /! あなたは要約を生成するAIです。
                /! 返答はせず、要約だけをしてください。
                
                /! フォーマットは以下の通りです。
                /! # タイトル
                /! ## 概要
                /! ## 詳細
                
                /! 解説は日本語でしてください。
                /! 以下のメッセージを要約してください。
                {messages}
                """,
                images,
            ],
        )

        # 要約の送信
        response_message = f"AIによる要約\n{response.text}"
        if len(response_message) > 2000:
            response_message = response_message[:2000] + "..."
        await ctx.followup.send(response_message)
        return


async def setup(bot: commands.Bot):
    await bot.add_cog(Summary(bot))
