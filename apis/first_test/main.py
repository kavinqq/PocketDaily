from flask import Blueprint


first_test_bp = Blueprint('first_test', __name__)


@first_test_bp.route("/")
def home():
    return "Hello! First Test App!"
