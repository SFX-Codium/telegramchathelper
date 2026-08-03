from pyrogram import Client
from config import *
from source import client   
from source import chatadmin
from source import parser
from source import profile
from source import animeapi
from pyrogram.handlers import MessageHandler


class MainApp:
    def __init__(self):
        self.app = Client(
            name=name,
            api_id=apiId,
            api_hash=apiHash,
            phone_number=phoneNumber,
            password=password,
        )
    
    def registerHandlers(self) -> None:
        self.app = client.Handler.reigsterHandlers(self.app)
        self.app = chatadmin.Handler.reigsterHandlers(self.app)
        self.app = profile.Handler.reigsterHandlers(self.app)
        self.app = animeapi.Handler.registerHandlers(self.app)


        self.app = parser.Parser.reigsterHandlers(self.app)
        #self.app.add_handler(MessageHandler(callback=))
    
    def startHelper(self):
        MainApp.registerHandlers(self)
        self.app.run()

if __name__ == "__main__":
    hp = MainApp()
    hp.startHelper()