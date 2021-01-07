from flask import render_template, jsonify, request

from grandpy import app
from grandpy.models.models import Parser

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/treat', methods=['POST'])
def treat_the_request():
    user_text = request.data.decode()
    response = Parser().clean(user_text)
    return jsonify(response)