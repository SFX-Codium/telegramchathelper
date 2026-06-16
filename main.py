from pyrogram import Client
from config import *
from source import client

class MainApp:
    def __init__(self):
        self.app = Client(
            name=name,
            api_id=apiId,
            api_hash=apiHash,
            app_version=version,
            phone_number=phoneNumber,
            password=password,
        )
    
    def registerHandlers(self) -> None:
        self.app = client.Handler.reigsterHandlers(self.app)
    
    def startHelper(self):
        MainApp.registerHandlers(self)
        self.app.run()

if __name__ == "__main__":
    hp = MainApp()
    hp.startHelper()