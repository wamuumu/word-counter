from flask import render_template, request, Response, redirect, url_for
from app import app 

import json
import time

monitorWords = []

@app.route('/', methods=['GET', 'POST'])
def data():
    global monitorWords

    if request.method == "GET":
        if len(monitorWords) == 0:
            return redirect(url_for('data'))
        return render_template('home.html',  words=monitorWords)

    elif request.method == "POST":
        request_data = request.get_json()
        monitorWords = json.loads(request_data)
        print(monitorWords)
        return Response("{'message':'words updated correctly'}", status=200, mimetype='application/json')
    
    else:
        return Response("{'message':'Bad request'}", status=400, mimetype='application/json')
