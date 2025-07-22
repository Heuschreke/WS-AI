from flask import Blueprint, render_template, request, redirect, url_for, current_app
from werkzeug.utils import secure_filename

import uuid
import os

bp = Blueprint('routes', __name__)



@bp.route("/")
def home():
    return render_template('index.html')

@bp.route('/upload', methods=['POST'])
def upload():
    if 'photo' not in request.files:
        return redirect('/')

    file = request.files['photo']
    if file.filename == '':
        return redirect('/')

    if not file.filename.lower().endswith(('.jpg', '.png', '.jpeg')):
        return "Только изображения (JPG/PNG)!"

    os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)

    filename = f"{uuid.uuid4()}_{secure_filename(file.filename)}"
    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
    return f'Файл {filename} загружен!'

def register_routes(app):
    app.register_blueprint(bp)