from pyrogram import Client
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatType
from pyrogram.handlers import MessageHandler
from config import myId, prefixCommand, clientCommands, profileCommands


class HandlerFilter:
    @staticmethod
    def meFilterFunction(_, __, message: Message): return message.from_user.id == myId
    meFilter = filters.create(name="filter", func=meFilterFunction)
    
    @staticmethod
    def commandFilterFunction(commands: list):
        def function(_, __, message: Message):
            if not (message.from_user and message.from_user.id == myId): return False
            if not (message.text is not None): return False
            if not (message.text.split(' ')[0] in commands): return False
            return True
        
        return function
    
    pointFilter = filters.create(name="pointFilter", func=commandFilterFunction([prefixCommand]))
    helloFilter = filters.create(name="helloFilter", func=commandFilterFunction([f"{prefixCommand}hi", f"{prefixCommand}hello", f"{prefixCommand}пр", f"{prefixCommand}привет"]))
    getIdFilter = filters.create(name="getIdFilter", func=commandFilterFunction([f"{prefixCommand}id", f"{prefixCommand}айди"]))


class MessageText:
    hello: str = "**👏 Всех приветствую!**"
    helloUser: str = "**👏 Привет, {0}!**"
    commandsList: str = f"""
**📚 Список команд TG helper chat:**\n
**{prefixCommand}** __вызвать это меню__
**{prefixCommand}hi** __поприветствовать__
**{prefixCommand}id** __получить id__
**{prefixCommand}msg** __показать сообщения ('{prefixCommand}msg -h' — просмотр всех флагов)__

Чат команды:
**{prefixCommand}cchat** __создать новую группу__
**{prefixCommand}dchat** __удалить группу__
**{prefixCommand}prom** __изменить права участника__
**{prefixCommand}warn** __выдать предупреждение__
**{prefixCommand}ban** __выдать блокировку__
**{prefixCommand}mbs** __список участников__

Профиль команды:
**{prefixCommand}ca** __поменять аватарку (Отправлять с изображением){" Доступно для всех." if profileCommands['cmdCaAll'] else ""}__

Аниме API:
**{prefixCommand}emotions** __список эмоций__
**{prefixCommand}aniq** __случайная цитата на английском__

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
        if clientCommands["cmdHello"]: client.add_handler(MessageHandler(callback=Handler.helloUser,   filters=HandlerFilter.helloFilter))
        if clientCommands["cmdHelp"]:  client.add_handler(MessageHandler(callback=Handler.helpCommand, filters=HandlerFilter.pointFilter))
        if clientCommands["cmdGetId"]: client.add_handler(MessageHandler(callback=Handler.getId,       filters=HandlerFilter.getIdFilter))
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