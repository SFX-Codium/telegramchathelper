from pyrogram import Client
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatType
from pyrogram.handlers import MessageHandler
from config import myId, prefixCommand


class HandlerFilter:
    @staticmethod
    def meFilterFunction(_, __, message: Message): return message.from_user.id == myId
    meFilter = filters.create(name="filter", func=meFilterFunction)
    
    @staticmethod
    def catFilterFunction(_, message: Message):
        isMe: bool = message.from_user and message.from_user.id == myId
        hasText: bool = message.text is not None
        isCommand: bool = message.text in [f"{prefixCommand}cat",
                                           f"{prefixCommand}кот"]
        return isMe and hasText and isCommand
    
    catFilter = filters.create(name="helloFilter", func=catFilterFunction)


class MessageText:
    captionCatImage: str = "**{0}, случайная картинка кота.**"


class Handler:
    @staticmethod
    def reigsterHandlers(client: Client) -> Client:
        client.add_handler(MessageHandler(callback=Handler.generateCatImage, filters=HandlerFilter.catFilter))
        return client
    
    
    @staticmethod
    async def generateCatImage(client: Client, message: Message) -> None:
        
        await client.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.id,
            text=MessageText.captionCatImage
        )