import base64
from crypt import methods
import os
from django.shortcuts import render
from flask import Flask, render_template, request, jsonify
import util
import mimetypes

app = Flask(__name__, template_folder='../template', static_folder='../template/static')

@app.route('/')
def index():
    return render_template('app.html')


@app.route('/uploadimg', methods=['POST'])
def uploadimg():
    image_data = request.files['img_file']
    encode_image = base64.b64encode(image_data.read())
    decode_image = encode_image.decode('utf-8')
    file_type = mimetypes.guess_type(image_data.filename)

    image_b64 = 'data:' + file_type[0] + ';base64,' + decode_image

    # with open("/media/darkdevil/2C3479B034797DA0/Data Science practice/celebrity_idetification/server/b64.txt") as f:
    #     test1 = f.read()

    response = jsonify(util.classify_image(image_b64, None))

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


if __name__ == "__main__":
    print("Starting the classifier app..")
    util.load_saved_artifacts()
    app.run(port=5000)
    app.run(debug=True)
