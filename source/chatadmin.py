from pyrogram import Client
from pyrogram import filters
from pyrogram.types import Message, ChatPrivileges
from pyrogram.enums import ChatType
from pyrogram.handlers import MessageHandler
from pyrogram.errors import BadRequest
from config import myId, prefixCommand, chatadminCommands

class MessageText:
    newGroupCreated: str = """**ℹ️ Группа {0} создана.**
Ссылка на группу: {1}
Дата создания: {2}"""
    howCreateGroup: str = f"**{prefixCommand}cchat [Название]** - __создать группу__."
    wrongTitle: str = "**⚠️ Неправильно набрано название группы, введите /dchat {title} для удаления группы**"
    howDeleteChat: str = "**/dchat [Название группы] - чтобы удалить группу, созданная вами.**"
    userHasBeenBanned: str = "**📛 Пользователь - __{0}__ забанен**"
    howBanUser: str = "**/ban** - исключить пользователя из группы"
    flagsPromote: str = f"""
**{prefixCommand}prom** - выдать участнику группы стутс администратора

**-mc** - управление чатом
**-dm** - удаление сообщений
**-mvc** - управление гч
**-rm** - управление участниками группы
**-pm** - управление администраторами
**-ci** - менять информацию чата
**-pin** - прикреплять сообщения
**-em** - изменять сообщения
**-iu** - приглашать участников
**-an** - анонимность администратора"""
    userGetAdmin: str = "**✅ Пользователь получил статус администратора**"
    userLostAdmin: str = "**✅ С пользователя снят статус администратора**"
    onlyChannelOrSuperGroup: str = "**❌ Эта команда работает только в супергруппах и каналах.**"
    allMembers: str = "**Пользователи чата: {0}**\n"
    onlyGroups: str = "**❌ Эта команда работает только в группах и супергруппах**"
 
    
class HandlerFilter:
    @staticmethod
    def commandFilterFunction(commands: list):
        def function(_, __, message: Message):
            if not (message.from_user and message.from_user.id == myId): return False
            if not (message.text is not None): return False
            if not (message.text.split(' ')[0] in commands): return False
            return True
        
        return function
    
    createChatFilter  = filters.create(name="createChatFilter",  func=commandFilterFunction([prefixCommand+"cchat", prefixCommand+"счат"]))
    deleteChatFilter  = filters.create(name="deleteChatFilter",  func=commandFilterFunction([prefixCommand+"dchat", prefixCommand+"учат"]))
    banUserFilter     = filters.create(name="banUserFilter",     func=commandFilterFunction([prefixCommand+"ban", prefixCommand+"бан"]))
    promoteUserFilter = filters.create(name="promoteUserFilter", func=commandFilterFunction([prefixCommand+"prom", prefixCommand+"perm", prefixCommand+"пром"]))
    getMembersFilter  = filters.create(name="getMembersFilter",  func=commandFilterFunction([prefixCommand+"mbs", prefixCommand+"учт"]))
    
    
class Handler:
    @staticmethod
    def checkFlags(flags: list, flag: str) -> bool:
        if flag in flags: return True
        else: return False
    
    @staticmethod
    def reigsterHandlers(client: Client) -> Client:
        if chatadminCommands['cmdCreateChat']:  client.add_handler(MessageHandler(callback=Handler.createChat,  filters=HandlerFilter.createChatFilter))
        if chatadminCommands['cmdDeleteChat']:  client.add_handler(MessageHandler(callback=Handler.deleteChat,  filters=HandlerFilter.deleteChatFilter))
        if chatadminCommands['cmdBanUser']:     client.add_handler(MessageHandler(callback=Handler.banUser,     filters=HandlerFilter.banUserFilter))
        if chatadminCommands['cmdPromoteUser']: client.add_handler(MessageHandler(callback=Handler.promoteUser, filters=HandlerFilter.promoteUserFilter))
        if chatadminCommands['cmdGetMembers']:  client.add_handler(MessageHandler(callback=Handler.getMembers,  filters=HandlerFilter.getMembersFilter))
        #client.add_handler(MessageHandler(callback=Handler.X, filters=HandlerFilter.X))
        return client

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
    
    @staticmethod
    async def deleteChat(client: Client, message: Message):
        try:
            chat_id = message.chat.id
            title = message.chat.title
            if " ".join(message.text.split(' ')[1:]) == title and len(message.text.split(' ')) > 1:
                await client.leave_chat(chat_id=chat_id, delete=True)
            elif " ".join(message.text.split(' ')[1:]) != title and len(message.text.split(' ')) > 1:
                await client.edit_message_text(chat_id=message.chat.id,
                                            message_id=message.id,
                                            text=MessageText.wrongTitle.format(title=message.chat.title))
            else:
                await client.edit_message_text(chat_id=message.chat.id,
                                            message_id=message.id,
                                            text=MessageText.howDeleteChat)
        except Exception as E:
            pass
    
    @staticmethod
    async def banUser(client: Client, message: Message):
        try:
            if message.reply_to_message:
                await client.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
                await client.edit_message_text(chat_id=message.chat.id,
                                            message_id=message.id,
                                            text=MessageText.userHasBeenBanned.format(message.reply_to_message.from_user.first_name))
            else:
                await client.edit_message_text(chat_id=message.chat.id,
                                            message_id=message.id,
                                            text=MessageText.howBanUser)
        except Exception as E:
            pass
    
    @staticmethod
    async def promoteUser(client: Client, message: Message):
        if not message.reply_to_message:
            await client.edit_message_text(
                chat_id=message.chat.id,
                message_id=message.id,
                text=MessageText.flagsPromote
            )
            return

        if message.chat.type not in [ChatType.SUPERGROUP, ChatType.CHANNEL]:
            await client.edit_message_text(
                chat_id=message.chat.id,
                message_id=message.id,
                text=MessageText.onlyChannelOrSuperGroup
            )
            return

        try:
            # Принудительно обновляем кэш чата, чтобы избежать CHANNEL_INVALID
            await client.get_chat(message.chat.id)

            flags = message.text.split(' ')
            privileges = ChatPrivileges(
                can_delete_messages=Handler.checkFlags(flags, '-dm'),
                can_restrict_members=Handler.checkFlags(flags, '-rm'),
                can_pin_messages=Handler.checkFlags(flags, '-pin'),
                can_invite_users=Handler.checkFlags(flags, '-iu'),
                can_promote_members=Handler.checkFlags(flags, '-pm'),
                can_manage_chat=Handler.checkFlags(flags, '-mc'),
                can_manage_video_chats=Handler.checkFlags(flags, '-mvc'),
                can_change_info=Handler.checkFlags(flags, '-ci'),
                can_edit_messages=Handler.checkFlags(flags, '-em'),
                is_anonymous=Handler.checkFlags(flags, '-an')
            )

            await client.promote_chat_member(
                chat_id=message.chat.id,
                user_id=message.reply_to_message.from_user.id,
                privileges=privileges
            )

            if len(flags) > 1:
                await client.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=message.id,
                    text=MessageText.userGetAdmin
                )
            else:
                await client.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=message.id,
                    text=MessageText.userLostAdmin
                )

        except Exception as E:
            await client.edit_message_text(
                chat_id=message.chat.id,
                message_id=message.id,
                text=f"❌ Произошла ошибка: {E}"
            )
    
    @staticmethod
    async def getMembers(client: Client, message: Message):
        try:
            nicknames: list = []
            async for member in client.get_chat_members(message.chat.id):
                nicknames.append(("👤 " if not member.user.is_bot else "🤖 ") + member.user.first_name + (member.user.last_name if member.user.last_name is not None else ''))
            
            await client.edit_message_text(
                chat_id=message.chat.id,
                message_id=message.id,
                text=MessageText.allMembers.format(message.chat.title)+'\n'.join(nicknames))
        except BadRequest:
            await client.edit_message_text(
                chat_id=message.chat.id,
                message_id=message.id,
                text=MessageText.onlyGroups)
        except Exception:
            pass