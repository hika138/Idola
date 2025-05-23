import discord
from discord.ext import commands
from google import genai
import cogs.MessageHandler as MessageHandler

# ある会話のレビューを生成するCog
# 使い方: /review <開始メッセージID> <終了メッセージID>
class Review(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.client: genai.Client = bot.client

    @discord.app_commands.command(
        name="review",
        description="レビューを生成します"
    )
    async def review(self, ctx: discord.Interaction, start: str, end: str):
        try:
            await ctx.response.defer()
        except discord.errors.NotFound:
            await ctx.edit_original_response("インタラクションがタイムアウトしました。")
            return
    # メッセージの取得
        messages, images = await MessageHandler.get_messages_by_period(ctx, start, end)
        contents = []
        contents.append(f"""
            /! から始まる行は会話ではなく命令です。必ず従ってください。
            
            /! あなたはDiscordのbotです。
            /! あなたは会話をレビューを生成するAIです。
            /! 会話の流れを確認して、論点や議論の脱線、誤解、誤った情報を指摘してください。
            /! 返答はせず、レビューだけをしてください。
            
            /! フォーマットは以下の通りです。
            /! # タイトル
            /! ## 概要
            /! ## 詳細
            /! ### 論点
            /! ### 問題点
            /! (ない場合は「なし」と記載してください)
            
            /! レビューは日本語でしてください。
            /! 以下のメッセージをレビューしてください。
            {messages}
        """)
        if images:
            contents.append(images)

        # レビューの生成
        response = self.client.models.generate_content(
            model="gemini-2.5-flash-preview-04-17",
            contents=contents,
        )

        # レビューの送信
        response_message = f"AIによるレビュー\n{response.text}"
        if len(response_message) > 2000:
            response_message = response_message[:2000] + "..."
        await ctx.followup.send(response_message)
        return
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Review(bot))