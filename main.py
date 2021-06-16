import os
from dotenv import load_dotenv
from server import Server
from handlers import handlers

load_dotenv()


def main():

    TOKEN= os.getenv('TOKEN')
    DB_URL= os.getenv('DATABASE_URL')
    PORT= os.getenv('PORT')
    URL= os.getenv('URL')
    LISTEN= os.getenv('LISTEN')

    server = Server(DB_URL,TOKEN,handlers)

    if URL:
        server.production(URL,PORT,LISTEN,TOKEN)

    else:
        server.development()    

if __name__ == '__main__':
    main()    
