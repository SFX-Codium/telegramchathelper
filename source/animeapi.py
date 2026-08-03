from aiofiles.os import stat
from pyrogram import Client
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler
from config import myId, prefixCommand, animeCommands
from source.apitools import commandFilterFunction

import requests
from requests import Response
from json import loads
from nekosbest import Client as NekoClient


class AnimeQuoteApi:
    baseUrl = "https://api.animechan.io/v1"
    randomeQuote = "/quotes/random"

    @staticmethod
    def getRandomeAnimeQuote() -> dict:
        response: Response = requests.get(AnimeQuoteApi.baseUrl+AnimeQuoteApi.randomeQuote)
        content: dict = response.json()
        return content


class NekoMediaApi:
    baseUrl = "https://nekos.best/api/v2/"

    emotionList: list = [
        ":^",
        "@-@", "@_@",
        ">:@",
        ">:(",
        ");",
        ":3",
        ":)",
        ":D",
        "<3",
        "XD",
        ":|",
        ":/",
        "o_o/",
        ":]",
        "-_-",
        "..."
    ]

    emotionDict: dict = {
        ":^": "hug",
        "@-@": "confused",
        "@_@": "confused",
        ">:@": "baka",
        ">:(": "angry",
        ");": "cry",
        ":3": "nya",
        ":)": "smile",
        ":D": "happy",
        "<3": "kiss",
        "XD": "laugh",
        ":|": "bored",
        ":/": "think",
        "o_o/": "wave",
        ":]": "teehee",
        "-_-": "facepalm",
        "...": "lurk"
    }

    @staticmethod
    async def getGif(category):
        async with NekoClient() as client:
            result = await client.get_image(category)
            return result.url


class HandlerFilter:
    animeRandomQuoteFilter = filters.create(name="animeRandomQuoteFilter", func=commandFilterFunction(commands=[prefixCommand+"aniq"]))
    NekoMediaApiFilter = filters.create(name="NekoMediaApiFilter", func=commandFilterFunction(commands=NekoMediaApi.emotionList))
    NekoMediaApiEmotionsListFilter = filters.create(name="NekoMediaApiEmotionsListFilter", func=commandFilterFunction(commands=[prefixCommand+"emotions"]))


class MessageText:
    quoteTemplate = "\"{0}</blockquote>\"\n\n__by {1} from «{2}»__"
    emotionsList = """Список всех эмодзи
```python
emotionDict: dict = {
    ":^": "hug",
    "@-@": "confused",
    "@_@": "confused",
    ">:@": "baka",
    ">:(": "angry",
    ");": "cry",
    ":3": "nya",
    ":)": "smile",
    ":D": "happy",
    "<3": "kiss",
    "XD": "laugh",
    ":|": "bored",
    ":/": "think",
    "o_o/": "wave",
    ":]": "teehee",
    "-_-": "facepalm",
    "...": "lurk"
}```
"""


class Handler:
    @staticmethod
    def registerHandlers(client: Client) -> Client:
        if animeCommands["cmdAniq"]: client.add_handler(MessageHandler(callback=Handler.animeRandomQuote, filters=HandlerFilter.animeRandomQuoteFilter))
        if animeCommands["animeEmotions"]: client.add_handler(MessageHandler(callback=Handler.NekoApiEmotions, filters=HandlerFilter.NekoMediaApiFilter))
        if animeCommands["animeEmotions"]: client.add_handler(MessageHandler(callback=Handler.NekoApiEmotionsList, filters=HandlerFilter.NekoMediaApiEmotionsListFilter))
        return client

    @staticmethod
    async def animeRandomQuote(client: Client, message: Message) -> None:
        quote = AnimeQuoteApi.getRandomeAnimeQuote()
        messageText: str = MessageText.quoteTemplate.format(
            quote["data"]["content"],
            quote["data"]["character"]["name"],
            quote["data"]["anime"]["name"]
        )
        await client.edit_message_text(
            chat_id=message.chat.id,
            text=messageText,
            message_id=message.id
        )
    
    @staticmethod
    async def NekoApiEmotions(client: Client, message: Message) -> None:
        gifUrl: str = await NekoMediaApi.getGif(category=NekoMediaApi.emotionDict[message.text])
        await message.delete()
        await client.send_animation(
            chat_id=message.chat.id,
            animation=gifUrl
        )
    
    @staticmethod
    async def NekoApiEmotionsList(client: Client, message: Message) -> None:
        await client.edit_message_text(
            chat_id=message.chat.id,
            text=MessageText.emotionsList,
            message_id=message.id
        )