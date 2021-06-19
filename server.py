from os import name
from telegram.ext import Updater
from db.database import Database
import logging

from actions.update_user import update


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


class Server:

    def __init__(self, db_url:str, token:str, handlers:dict):
        self.updater = Updater(token)
        self.dispatcher = self.updater.dispatcher
        self.dispatcher.bot_data["database"] = Database(db_url)
        self.dispatcher.job_queue.run_repeating(update,900,first=1,context=self.dispatcher.bot_data["database"],name="update_user")
        self.handler(handlers)


    def handler(self, handlers:dict):

        for type,handle_list in handlers.items():
            for handle in handle_list:
                kwargs = handle[0]
                self.dispatcher.add_handler(type(**kwargs))


    def production(self, url:str, port:int, listen:str, token:str):

        self.updater.start_webhook(
            listen=listen, 
            port=port, 
            url_path=token, 
            webhook_url=f"{url}/{token}"
            )         

        logging.info(f"started listening at port : {port}")
        self.updater.idle()


    def development(self):

        self.updater.start_polling()
        logging.info("Started polling")
        self.updater.idle() 
      

      

                

