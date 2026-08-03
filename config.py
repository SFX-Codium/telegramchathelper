#
#   Приветсвтую вас в файле конфигурации приложения.
#   К каждому параметру будет предоставлен комментарий с пояснением.
#   

# - Auth
# Как получить данные phoneNumber, apiId, apiHash - смотреть в README.md
apiId: int
apiHash: str
phoneNumber: str # Формат "+7 aaa bbb ddcc", "+7aaabbbddcc и т.п."
password: str # Пароль от телегармм аккаунта
myId: int # Ваш телеграмм id

# Название файла / сессии
sessionName: str = "tghelper"
name = sessionName

# - App
# Логирование программы, по умолчанию False
# Функция будет добавлена в следующих обновлениях
logOn: bool = False

# Версия приложения (Мета данные)
version: str = "v1.0"

# - Functional (True - команда включена, False - выключена)
# Префикс для команд, по умолчанию ".". Префикс определяет,
# пишите вы команду или же обычный текст, некий активатор команд.
prefixCommand: str = "!"
clientCommands: dict = {
    "cmdHelp":  True, # Сообщение с помощью
    "cmdHello": True, # Приветствие
    "cmdGetId": True, # Получить ID чата и свой + пользователя
}

chatadminCommands: dict = {
    "cmdCreateChat":  True, # Создать чат
    "cmdDeleteChat":  True, # Удалить чат
    "cmdBanUser":     True, # Блокировка пользователя
    "cmdPromoteUser": True, # Назначение админом
    "cmdGetMembers":  True  # Получить список участников
}

parserCommands: dict = {
    "cmdDb": True # Все сообщения
}

profileCommands: dict = {
    "cmdCa": True,    # Команда, которая меняет аву
    "cmdCaAll": True, # True команада для всех, False только пользователю
    "cmdCn": True,    # Команда, которая меняет Имя
    "cmdCnAll": True, # True команада для всех, False только пользователю
}

animeCommands: dict = {
    "cmdAniq": True,
    "animeEmotions": True
}