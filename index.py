from flask import (
    Flask,
    request,
    abort,
    render_template,
)
from linebot import WebhookHandler
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent,
    TextMessage,
)

from models import db, migrate
from apis.event_center.main import EventCenter
from log_config import setup_logging
from config import Config


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)

setup_logging()
line_handler = WebhookHandler(app.config["CHANNEL_SECRET"])


@app.route("/")
def home():
    app.logger.info("訪問首頁！")
    return render_template("index.html")


"""
所有從LINE平台發送的事件都會發送到這個路由上，這個路由會將事件轉發給handler進一步處理。
"""
@app.route("/webhook", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)

    app.logger.info("Request body: " + body)

    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

"""
Handler在收到事件後，會根據定義的行為來做出對應的處理。
因此我們會需要在這個區塊中定義我們的行為。
"""
@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    event_center = EventCenter()
    event_center.handle_event(event)
    

if __name__ == "__main__":
    app.run(debug=False)
