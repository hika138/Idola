from datetime import timedelta
import discord

async def get_messages_by_period(ctx: discord.Interaction, start: str, end: str) -> str:
    # メッセージIDが数字かどうかを確認
    if not start.isdecimal() or not end.isdecimal():
        await ctx.followup.send("メッセージIDは数字で指定してください。")
        return
    # startとendのメッセージIDを取得
    try:
        start_message = await ctx.channel.fetch_message(int(start))
        end_message = await ctx.channel.fetch_message(int(end))
    except discord.NotFound:
        await ctx.followup.send("指定されたメッセージが見つかりません。")
        return
    # メッセージの取得と整形
    messages = [f'{message.author.display_name}({message.author.id}): {message.content}' async for message in ctx.channel.history(before=end_message.created_at + timedelta(seconds=1), after=(start_message.created_at - timedelta(seconds=1)), limit=2000)]
    messages = "\n".join(messages)
    if len(messages) > 2000:
        messages = messages[:2000] + "..."
    return messages