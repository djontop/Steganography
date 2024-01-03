from flask import Flask, render_template, request, redirect, url_for
from stegano import lsb
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encode', methods=['POST'])
def encode():
    if 'image' not in request.files or 'message' not in request.form:
        return redirect(url_for('index'))

    image_data = request.files['image'].stream.read()
    
    image_file = BytesIO(image_data)

    secret_image = lsb.hide(image_file, request.form['message'])

    secret_image.save('static/secret.png')

    return render_template('result.html', image_path='static/secret.png')

@app.route('/decode')
def decode():
    return render_template('decode.html')

@app.route('/decode_result', methods=['POST'])
def decode_result():
    if 'image' not in request.files:
        return redirect(url_for('decode'))

    image_data = request.files['image'].stream.read()

    image_file = BytesIO(image_data)

    secret_message = lsb.reveal(image_file)

    return render_template('decode_result.html', secret_message=secret_message)

if __name__ == '__main__':
    app.run(debug=True)
