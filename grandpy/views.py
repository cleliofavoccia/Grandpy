from flask import render_template, jsonify, request
import os

from grandpy import app
from grandpy.models import Grandpy

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", google_key=os.getenv('JAVASCRIPT_API_KEY'))

@app.route('/response', methods=['POST'])
def response_to_request():
    user_text = request.data.decode()
    response = Grandpy().give_infos(user_text)
    return jsonify(response)