from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerMessage, StickerSendMessage
)


app = Flask(__name__)

line_bot_api = LineBotApi('ox9nyMEfrgcFd+jFp09zADrGb2ssHdV+tThfhBn7Dtwq9Ugtf0guKBydMWRZgELbaf+neE4QFBIlZF5rqrZp//Xneqw2Be0oAX/f3LEcs2SxF+9Ii+jAMhXn+lovPquYwPfRRfKEUTCf78zBBjyqGgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('60a27f9127fc781cb833b6809e0643d1')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event.message.text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id=event.message.package_id,
            sticker_id=event.message.sticker_id)
    )


if __name__ == "__main__":
    app.debug=True
    app.run(host='localhost',port=800)