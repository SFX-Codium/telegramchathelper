from config import myId, prefixCommand


async def send_long_message(client, chat_id, text, **kwargs):
    limit = 4096
    
    parts = [text[i:i + limit] for i in range(0, len(text), limit)]
    
    for part in parts:
        await client.send_message(chat_id, part, **kwargs)


def commandFilterFunction(commands):
    def function(_, __, message):
        if not (message.from_user and message.from_user.id == myId): return False
        if not (message.text is not None): return False
        if not (message.text.split(' ')[0] in commands): return False
        return True
        
    return function