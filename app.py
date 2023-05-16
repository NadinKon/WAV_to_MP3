from flask import Flask, request, jsonify, send_file
from models import User, Audio, db
from audio_processing import convert_to_mp3
import uuid

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db/mydb'
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app


app = create_app()

# Создание нового пользователя
@app.route('/users', methods=['POST'])
def create_user():
    # Получаем имя из запроса
    name = request.json.get('name')

    # Если имя не предоставлено, возвращаем ошибку
    if not name:
        return jsonify({"error": "No name provided"}), 400

    # Создаем нового пользователя с уникальным токеном
    user = User(name=name, token=str(uuid.uuid4()))

    # Добавляем пользователя в базу
    db.session.add(user)
    db.session.commit()

    # Возвращаем ID пользователя и токен
    return jsonify({"user_id": user.id, "token": user.token}), 201


# Добавление новой аудиозаписи
@app.route('/audios', methods=['POST'])
def add_audio():
    # Получаем ID пользователя, токен и аудиозапись из запроса
    user_id = request.json.get('user_id')
    token = request.json.get('token')
    audio_data = request.files.get('audio')

    # Получаем пользователя из базы данных
    user = User.query.get(user_id)

    # Если пользователь не существует или токен неверный, возвращаем ошибку
    if not user or user.token != token:
        return jsonify({"error": "Invalid user or token"}), 401

    # Конвертируем аудиозапись в формат mp3
    mp3_data = convert_to_mp3(audio_data)

    # Создаем новую аудиозапись с уникальным ID
    audio = Audio(id=str(uuid.uuid4()), data=mp3_data, user_id=user_id)

    # Добавляем аудиозапись в базу данных
    db.session.add(audio)
    db.session.commit()

    # Возвращаем URL для скачивания записи
    return jsonify({"url": f"http://host:port/record?id={audio.id}&user={user_id}"}), 201


# Получения аудиозаписи
@app.route('/record', methods=['GET'])
def get_audio():
    # Получаем ID аудиозаписи и пользователя из запроса
    audio_id = request.args.get('id')
    user_id = request.args.get('user')

    # Получаем аудиозапись из базы данных
    audio = Audio.query.get(audio_id)

    # Если аудиозапись не существует или ID пользователя неверный, возвращаем ошибку
    if not audio or audio.user_id != user_id:
        return jsonify({"error": "Invalid audio id or user id"}), 404

    # Возвращаем аудиозапись
    return send_file(audio.data, mimetype='audio/mp3')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
