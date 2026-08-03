from pyrogram import Client
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.types.messages_and_media.message import Message as MessagePhoto
from pyrogram.enums import ChatType
from pyrogram.handlers import MessageHandler
from config import myId, prefixCommand, profileCommands
from source.apitools import commandFilterFunction

class HandlerFilter:
    @staticmethod
    def changeAvatarFilterFunction(*args):
        for context in args:
            if not isinstance(context, MessagePhoto):
                continue
            
            if profileCommands["cmdCaAll"]:
                if not (context.from_user): return False
            else:
                if not (context.from_user and context.from_user.id == myId): return False
            if not (context.caption is not None): return False
            if not (context.caption.split(' ')[0] in [f'{prefixCommand}ca']): return False
            return True
        return False
    
    changeAvatarFilter = filters.create(name="changeAvatarFilter", func=changeAvatarFilterFunction)


class MessageText:
    avatarHasBeenChanged: str = "**Аватарка успешно поменялась** :3"


class Handler:
    @staticmethod
    def reigsterHandlers(client: Client) -> Client:
        if profileCommands["cmdCa"]: client.add_handler(MessageHandler(callback=Handler.changeAvatarHandler, filters=HandlerFilter.changeAvatarFilter))
        #if profileCommands["cmdHelp"]:  client.add_handler(MessageHandler(callback=Handler.helpCommand, filters=HandlerFilter.pointFilter))
        #if profileCommands["cmdGetId"]: client.add_handler(MessageHandler(callback=Handler.getId,       filters=HandlerFilter.getIdFilter))
        return client

    @staticmethod
    async def changeAvatarHandler(client: Client, message: Message | MessagePhoto) -> None:
        path = await client.download_media(message.photo.file_id)
        await client.set_profile_photo(photo=path)
        await client.send_message(
            chat_id=message.chat.id,
            text=MessageText.avatarHasBeenChanged
        )