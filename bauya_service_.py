from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, ImageMessage)
import json
import time
from bauya import Bauya

# Line Preprocessing
secretFileContentJson = json.load(open("./secret.txt",'r'))
server_url = secretFileContentJson.get("server_url")
line_bot_api = LineBotApi(secretFileContentJson.get("Channel_access_token"))
handler = WebhookHandler(secretFileContentJson.get("Channel_secret"))

# Classifier Preparation
bau_judge = Bauya()

# Server Perprocessing
app = Flask(__name__, static_url_path = "/images" , static_folder = "./")

@app.route("/", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=ImageMessage)
def handle_message(event):
    message_content = line_bot_api.get_message_content(event.message.id)
    f = './'+event.message.id+'.jpg'
    with open(f, 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)
    
    _, cs = bau_judge.judge(f)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=cs))

# main
app.run()