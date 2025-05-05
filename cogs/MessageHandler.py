from datetime import timedelta
import discord
import requests
from io import BytesIO
from PIL import Image

# ある期間のメッセージを取得する関数
async def get_messages_by_period(ctx: discord.Interaction, start: str, end: str) -> tuple[str, list]:
    # メッセージIDが数字かどうかを確認
    if not start.isdecimal() or not end.isdecimal():
        await ctx.followup.send("メッセージIDは数字で指定してください。")
        return "", []
    
    # startとendのメッセージIDを取得
    try:
        start_message = await ctx.channel.fetch_message(int(start))
        end_message = await ctx.channel.fetch_message(int(end))
    except discord.NotFound:
        await ctx.followup.send("指定されたメッセージが見つかりません。")
        return "", []
    
    # メッセージの取得と整形
    return_messages = []
    image_urls = []
    
    messages: list[discord.Message] = [message async for message in ctx.channel.history(before=end_message.created_at + timedelta(seconds=1), after=(start_message.created_at - timedelta(seconds=1)), limit=2000)]
    return_messages.append(f"チャンネル名: {ctx.channel.name}({ctx.channel.id})")
    
    # メッセージの取得
    for message in messages:
        return_messages.append(f"{message.author.display_name}({message.author.id}): {message.content}")
        
        # メッセージの添付ファイルを取得
        if message.attachments:
            for attachment in message.attachments:
                return_messages.append(f"添付ファイル: {attachment.url}")
                image_urls.append(attachment.url)
    
    # 画像の取得
    images = load_images_from_urls(image_urls)
    
    # メッセージの整形
    return_messages = "\n".join(return_messages)
    
    # メッセージが空の場合はエラーメッセージを返す
    if not return_messages:
        await ctx.followup.send("指定された期間にメッセージがありません。")
        return "", []
    
    # メッセージが2000文字を超える場合は切り捨て
    if len(return_messages) > 2000:
        return_messages = return_messages[:2000] + "..."
    return return_messages, images

def load_images_from_url(image_url: str) -> Image.Image | None:
    """
    指定されたURLから画像をダウンロードし、PIL Imageオブジェクトとして読み込みます。

    Args:
        image_url: 画像のURL。

    Returns:
        PIL Imageオブジェクト、またはダウンロードや読み込みに失敗した場合はNone。
    """
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # HTTPエラーが発生した場合に例外を発生させる
        img = Image.open(BytesIO(response.content))
        return img
    except requests.exceptions.RequestException:
        return None
    except IOError:
        return None

def load_images_from_urls(image_urls: list[str]) -> list[Image.Image]:
    """
    URLのリストから画像を読み込み、PIL Imageオブジェクトのリストを返します。

    Args:
        image_urls: 画像URLのリスト。

    Returns:
        読み込みに成功したPIL Imageオブジェクトのリスト。
    """
    images = []
    for url in image_urls:
        img = load_images_from_url(url)
        if img:
            images.append(img)
    return images