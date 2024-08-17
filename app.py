from flask import Flask, request, abort
from app import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

number = 1
# int number = 1
boolean = True
if number > 1:
    print("123")
else:
    print("456")



line_bot_api = LineBotApi('pJihqrzZVq1Ijw6MroQDqyOq5OlflrO7r831Zukg1flZWrzSYGJ9M0TNozT6TRE+qlpqiSL/DwSr7FliBjsgIsP7klx4rM6ajHGfRsuoVToySNnM7o2v5MauCDPHSQnCWgeYfBvb//A0BhiAXwFhjwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('976b22cb48db00f4c52c9c2d362c11f5')

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

if __name__ == "__main__":
    app.run()
