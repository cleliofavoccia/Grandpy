"""Contains all the views of the application"""
import os

from flask import jsonify, render_template, request

from grandpy import app
from grandpy.models import Grandpy


@app.route('/')
@app.route('/index')
def index():
    """Print of the file index.html in the route / and /index"""
    return render_template("index.html",
                           google_key=os.getenv('JAVASCRIPT_API_KEY'))


@app.route('/response', methods=['POST'])
def response_to_request():
    """Print of requests results from user requests in AJAX"""
    user_text = request.data.decode()
    response = Grandpy().give_infos(user_text)
    return jsonify(response)
