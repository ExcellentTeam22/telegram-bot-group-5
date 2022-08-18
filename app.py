from flask import Flask, Response, request
import requests

app = Flask(__name__)


@app.route('/sanity')
def sanity(): return "Server is running"


@app.route('/message', methods=["POST"])
def handle_message():
    print("got message")
    chat_id = request.get_json()['message']['chat']['id']
    res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'"
                       .format(TOKEN, chat_id, "Got it"))
    return Response("success")


TOKEN = ''
NGROK = 'https://beea-2a02-6680-1109-9609-6d7b-5f1b-f8ec-bc71.eu.ngrok.io'
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url={}/message'.format(
    TOKEN, NGROK)
requests.get(TELEGRAM_INIT_WEBHOOK_URL)


if __name__ == '__main__':
    app.run(port=5002)
