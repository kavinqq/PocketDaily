import os
from flask import Flask, request, abort
from apis.first_test.main import first_test_bp
from linebot import (
    LineBotApi,
    WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
)


app = Flask(__name__)
app.register_blueprint(first_test_bp, url_prefix="/first_test")

line_bot_api = LineBotApi(os.getenv("LineToken"))
handler = WebhookHandler(os.getenv('LineChannelSecret'))


@app.route("/")
def home():
    return "Hello! Main App!"


"""
所有從LINE平台發送的事件都會發送到這個路由上，這個路由會將事件轉發給handler進一步處理。
"""
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)

    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

"""
Handler在收到事件後，會根據定義的行為來做出對應的處理。
因此我們會需要在這個區塊中定義我們的行為。
"""
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )


if __name__ == "__main__":
    app.run(debug=False)
