from flask import Flask, Response, request
import requests
import face_recognition

app = Flask(__name__)
TOKEN = ''
NGROK = 'https://bab6-82-80-173-170.eu.ngrok.io'
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url={}/message'.format(TOKEN, NGROK)
requests.get(TELEGRAM_INIT_WEBHOOK_URL)


@app.route('/sanity')
def sanity(): return "Server is running"


@app.route('/message', methods=["POST"])
def handle_message():
    print("got message")
    json = request.get_json()
    chat_id = json['message']['chat']['id']
    message = json['message']['text']
    res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'".format(TOKEN, chat_id, message))
    return Response("success")


if __name__ == '__main__':
    app.run(port=5002)
    import face_recognition

    known_image = face_recognition.load_image_file("resources/4.jpg")
    unknown_image = face_recognition.load_image_file("resources/2.jpg")

    biden_encoding = face_recognition.face_encodings(known_image)[0]
    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

    results = face_recognition.compare_faces([biden_encoding], unknown_encoding)
    print(results)