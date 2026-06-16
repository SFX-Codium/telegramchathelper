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
    def pointFilterFunction(_, message: Message):
        if not (message.from_user and message.from_user.id == myId): return False
        if not (message.text is not None): return False
        if not (message.text == prefixCommand): return False
        return True
    pointFilter = filters.create(name="pointFilter", func=pointFilterFunction)
    
    @staticmethod
    def helloFilterFunction(_, message: Message):
        if not (message.from_user and message.from_user.id == myId): return False
        if not (message.text is not None): return False
        if not (message.text in [f"{prefixCommand}hi",
                                 f"{prefixCommand}hello",
                                 f"{prefixCommand}пр",
                                 f"{prefixCommand}привет"]): return False
        return True
    helloFilter = filters.create(name="helloFilter", func=helloFilterFunction)

    @staticmethod
    def createChatFilterFunction(_, message: Message):
        if not (message.from_user and message.from_user.id == myId): return False
        if not (message.text is not None): return False
        if not (message.text.split(' ')[0] in [f"{prefixCommand}cchat", f"{prefixCommand}счат"]): return False
        return True
    createChatFilter = filters.create(name="createChatFilter", func=createChatFilterFunction)
    
    @staticmethod
    def getIdFilterFunction(_, message: Message):
        if not (message.from_user and message.from_user.id == myId): return False
        if not (message.text is not None): return False
        if not (message.text in [f"{prefixCommand}id",
                                 f"{prefixCommand}айди"]): return False
        return True
    getIdFilter = filters.create(name="getIdFilter", func=getIdFilterFunction)

class MessageText:
    hello: str = "**👏 Всех приветствую!**"
    helloUser: str = "**👏 Привет, {0}!**"
    commandsList: str = f"""**📚 Список команд TG helper chat:**\n
**{prefixCommand}** __вызвать это меню__
**{prefixCommand}hi** __поприветствовать__
**{prefixCommand}cchat** __создать новую группу__
**{prefixCommand}id** __получить id__

__Бот создан **[SFX Codium](https://t.me/sfxcodium)**.__"""
    newGroupCreated: str = """**ℹ️ Группа {0} создана.**
Ссылка на группу: {1}
Дата создания: {2}"""
    howCreateGroup: str = f"**{prefixCommand}cchat [Название]** - __создать группу__."
    chatId: str = "__ID чата:__ `{0}`\n__Мой ID:__ `{1}`"
    fullChatId: str = "__ID чата:__ `{0}`\n__Мой ID:__ `{1}`\n__ID Пользователя:__ `{2}`"
    

class Handler:
    @staticmethod
    def reigsterHandlers(client: Client) -> Client:
        client.add_handler(MessageHandler(callback=Handler.helloUser, filters=HandlerFilter.helloFilter))
        client.add_handler(MessageHandler(callback=Handler.helpCommand, filters=HandlerFilter.pointFilter))
        client.add_handler(MessageHandler(callback=Handler.createChat, filters=HandlerFilter.createChatFilter))
        client.add_handler(MessageHandler(callback=Handler.getId, filters=HandlerFilter.getIdFilter))
        return client
    
    @staticmethod
    async def helpCommand(client: Client, message: Message) -> None:
        await client.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.id,
            text=MessageText.commandsList,
            disable_web_page_preview=True
        )
    
    @staticmethod
    async def helloUser(client: Client, message: Message) -> None:
        if message.reply_to_message:
            userTo = message.reply_to_message.from_user
            name: str = f"{userTo.first_name} {userTo.last_name}" if userTo.last_name is not None else str(userTo.first_name)
            messageText = MessageText.helloUser.format(name)
        else:
            messageText = MessageText.hello
        
        await client.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.id,
            text=messageText
        )
    
    @staticmethod
    async def createChat(client: Client, message: Message):
        try:
            chat = await client.create_group(title=" ".join(message.text.split(' ')[1:]), users=myId)
            link = await client.create_chat_invite_link(chat_id=chat.id)
            await client.edit_message_text(
                chat_id=message.chat.id,
                message_id=message.id,
                text=MessageText.newGroupCreated.format(chat.title, link.invite_link, link.date))
        except Exception as E:
            await client.edit_message_text(
                chat_id=message.chat.id,
                message_id=message.id,
                text=MessageText.howCreateGroup)
            print(E)
    
    @staticmethod
    async def getId(client: Client, message: Message):
        chatId: int = message.chat.id
        if message.reply_to_message:
            messageText: str = MessageText.fullChatId.format(chatId, myId, message.reply_to_message.from_user.id)
        else:
            messageText: str = MessageText.chatId.format(chatId, myId)
        
        await client.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.id,
            text=messageText
        )