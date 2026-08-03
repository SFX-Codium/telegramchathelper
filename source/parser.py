from pyrogram import Client
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler
from config import myId, prefixCommand, parserCommands
from source.database import get_db
from source.apitools import send_long_message

import aiosqlite

class Filter:
    keyWordArgs: dict[str, str] = {
        "-c": "chatTitle = '{0}' ",
        "-C": "chatId = '{0}' ",
        "-i": "userId = '{0}' ",
        "-u": "userUsername = '{0}' ",
        "-n": "userFullName = '{0}' "
    }

    @staticmethod
    def commandFilterFunction(commands: list):
        def function(_, __, message: Message):
            if not (message.from_user and message.from_user.id == myId): return False
            if not (message.text is not None): return False
            if not (message.text.split(' ')[0] in commands): return False
            return True
        
        return function

    def parserFilterFunction(_, __, message: Message):
        if message.text is not None:
            return True
        else:
            return False
    
    parserFilter       = filters.create(name="parserFilter", func=parserFilterFunction)
    getMessagesFilter  = filters.create(name="getMessagesFilter",  func=commandFilterFunction([prefixCommand+"db", prefixCommand+"дб", prefixCommand+"msg",]))

class Parser:
    @staticmethod
    def reigsterHandlers(client: Client) -> Client:
        if parserCommands["cmdDb"]: client.add_handler(MessageHandler(callback=Parser.outputMessages, filters=Filter.getMessagesFilter))
        client.add_handler(MessageHandler(callback=Parser.getMessage,     filters=Filter.parserFilter))
        return client
    

    @staticmethod
    async def getMessage(client: Client, message: Message) -> None:
        chatId        = message.chat.id
        chatTitle     = message.chat.title
        userId        = message.from_user.id
        userUsername  = message.from_user.username
        userFullName  = message.from_user.first_name + (" "+message.from_user.last_name if message.from_user.last_name is not None else "")
        userIsPremium = message.from_user.is_premium
        userIsBot     = message.from_user.is_bot
        messageId     = message.id
        messageText   = message.text
        messageDate   = message.date
        
        async with get_db() as conn:
            await conn.execute("INSERT INTO messages (chatId, chatTitle, userId, userUsername, userFullName, userIsPremium, userIsBot, messageId, messageText, messageDate) VALUES (?,?,?,?,?,?,?,?,?,?)", (
                chatId,
                chatTitle,
                userId,
                userUsername,
                userFullName,
                userIsPremium,
                userIsBot,
                messageId,
                messageText,
                messageDate,
            ))
            await conn.commit()

    @staticmethod
    async def outputMessages(client: Client, msg: Message) -> None:
        args: list[str] = msg.text.split(" ")
        requestFilter = "WHERE "
        
        if len(args) > 1:
            if args[1] in ["-h", "--help", "help"]:
                await client.edit_message_text(
                    chat_id=msg.chat.id,
                    message_id=msg.id,
                    text="**ℹ️ Все флаги для команды:**\n-h → список флагов\n-c → фильтровать по названию чата\n-C → фильтровать по ID чата\n\
-i → фильтр по ID пользователя\n-u → фильтр по username\n-n → фильтр по полному имени и фамилии"
                )
                return

            args.pop(0)
            
            for arg in args:
                if arg in Filter.keyWordArgs:
                    try:
                        flag: str = arg
                        key: str = Filter.keyWordArgs[flag]
                        indexValue: int = int(args.index(flag) + 1)
                        value: str = args[indexValue]

                        requestFilter: str = requestFilter + key.format(value)
                    except:
                        continue
        
        listMessages: list = []

        async with get_db() as conn:
            if requestFilter == "WHERE ":
                requestFilter = ""
            else:
                pass

            cursor = await conn.execute("SELECT * FROM messages " + requestFilter)
            messages = await cursor.fetchall()

            for message in messages:
                listMessages.append((f"[ {message[1]} ] " if message[1] is not None else "") + f"{message[4]} → {message[8]}")

        await client.edit_message_text(
            chat_id=msg.chat.id,
            message_id=msg.id,
            text="**ℹ️ Список всех последних сообщений:**"
        )

        await send_long_message(
            client,
            chat_id=msg.chat.id,
            text="\n".join(listMessages)
        )