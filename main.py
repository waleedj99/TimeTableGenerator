from flask import Flask, request, render_template, jsonify
import json
import random
import itertools
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        pass
if __name__ == '__main__':
    app.run(debug=True)
