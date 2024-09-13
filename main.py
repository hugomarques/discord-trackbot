import os
from dotenv import load_dotenv
from bot.client import bot
from flask import Flask

if os.path.exists('.env'):
    load_dotenv()

app = Flask(__name__)

@app.route('/health')
def health_check():
    return 'OK', 200

if __name__ == '__main__':
    from threading import Thread
    thread = Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': int(os.getenv('PORT', 5000))})
    thread.start()
    bot.run(os.getenv('DISCORD_TOKEN'))
