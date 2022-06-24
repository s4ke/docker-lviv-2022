from ai.runtime import classify
from flask import Flask, request
import logging


app = Flask(__name__)
logger = logging.getLogger(__name__)

@app.route("/classify", methods=['POST'])
@app.errorhandler(500)
def post_classify(*args):
    if 'image' not in request.files:
        return {
            "error": "no image present in request body"
        }, 400
    return classify(request.files["image"]), 200