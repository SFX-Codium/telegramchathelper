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
sessionName: str = "tgchathelper"
name = sessionName

# - App
# Логирование программы, по умолчанию False
# Функция будет добавлена в следующих обновлениях
logOn: bool = False

# Версия приложения (Мета данные)
version: str = "v1.0"

# - Functional
# Префикс для команд, по умолчанию ".". Префикс определяет,
# пишите вы команду или же обычный текст, некий активатор команд.
prefixCommand: str = "!"