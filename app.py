from flask import Flask, Response, request
import face_recognition
import requests

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

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

    known_face = face_recognition.face_encodings(face_recognition.load_image_file("resources/4.jpg"))[0]
    unknown_faces = face_recognition.face_encodings(message)
    match_results = face_recognition.compare_faces(unkown_face for unkown_face in unknown_faces
                                                   if face_recognition.compare_faces([known_face], unkown_face))
    res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'".format(TOKEN, chat_id,
                                                                                               "ANI 0-5-2-5-3-8-1-6-4-8"
                                                                                               if match_results else "MI ZOT?!"))
    return Response("success")


if __name__ == '__main__':
    app.run(port=5002)

    # biden_encoding = face_recognition.face_encodings(known_image)[0]
    # unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

    # results = face_recognition.compare_faces([biden_encoding], unknown_encoding)
    # print(results)
