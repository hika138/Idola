import discord
from discord.ext import commands
from google import genai



from datetime import timedelta

class Summary(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.client: genai.Client = bot.client
    
    @discord.app_commands.command(
        name="summary",
        description="要約を生成します"
    )
    async def summary(self, ctx: discord.Interaction, start: str, end: str):
        # メッセージの取得
        await ctx.response.defer()
        if not start.isdecimal() or not end.isdecimal():
            await ctx.followup.send("メッセージIDは数字で指定してください。")
            return
        try:
            start_message = await ctx.channel.fetch_message(int(start))
            end_message = await ctx.channel.fetch_message(int(end))
            print(start_message.created_at, end_message.created_at)
        except discord.NotFound:
            await ctx.followup.send("指定されたメッセージが見つかりません。")
            return
        messages = [f'{message.author.display_name}({message.author.id}): {message.content}' async for message in ctx.channel.history(before=end_message.created_at + timedelta(seconds=1), after=(start_message.created_at - timedelta(seconds=1)), limit=2000)]
        # メッセージの整形
        messages = "\n".join(messages)
        # 要約の生成
        print(messages)
        response = self.client.models.generate_content(
            model="gemini-2.5-flash-preview-04-17",
            contents=
            f"""
                /! から始まる行は会話ではなく命令です。必ず従い、次回以降の会話に反映してください。
                
                /! あなたは要約を生成するAIです。
                /! 返答はせず、要約だけをしてください。
                
                /! フォーマットは以下の通りです。
                /! # タイトル
                /! ## 概要
                /! ## 詳細
                
                /! 解説は日本語でしてください。
                /! 以下のメッセージを要約してください。
                {messages}
            """
        )
        
        # 要約の送信
        response_message = f"AIによる要約\n{response.text}"
        await ctx.followup.send(response_message)
        return

async def setup(bot: commands.Bot):
    await bot.add_cog(Summary(bot))
