## WAV_to_MP3
Сервис выполняющий следующие функции:
Создает пользователя, для каждого пользователя - сохраненяет аудиозаписи в формате wav, преобразовает её в формат mp3. <br>
Далее записывает в базу данных и предоставляет ссылки для скачивания аудиозаписи.

### Установка и запуск:
Клонируйте репозиторий и перейдите в рабочую директорию

git clone https://github.com/NadinKon/WAV_to_MP3 <br>
cd WAV_to_MP3

### Соберите образы Docker Compose и запустите контейнеры:
docker-compose up -d --build

### Использование:
Приложение теперь запущено и доступно по адресу http://localhost:5000

### Пример POST-запроса:
Создание пользователя:<br>
Отправьте POST-запрос на /users с JSON-объектом, содержащим имя пользователя. <br>
Например: {"name": "username"} <br>
Пример запроса через Powershell Windows: Invoke-WebRequest -Uri http://localhost:5000/users -Method POST -Body '{"name":"John"}' -ContentType "application/json"

В ответе получаем: {"token":"ff55919d-18bc-48a3-9afc-275faeb360ba","user_id":1} 

Добавление аудиозаписи: <br>
Отправьте POST-запрос на /audios с ID пользователя, токеном и аудиозаписью. <br>
Например: {"user_id": "user_id", "token": "token"} и прикрепите аудиозапись в формате WAV. <br>
Или вариант curl -X POST -H "Content-Type: multipart/form-data" -F "audio=@path_to_your_file.wav" -F "metadata={\"user_id\": \"your_user_id\", \"token\": \"your_token\"};type=application/json" http://localhost:5000/audios  <br>
В этом примере path_to_your_file.wav - это путь к вашему аудиофайлу <br>
your_user_id - это идентификатор пользователя <br>
your_token - это токен пользователя (нужно заменить на соответствующие значения, полученные ранее)

Получение аудиозаписи:<br>
Отправьте GET-запрос на /record с ID аудиозаписи и ID пользователя. <br>
Например: http://localhost:5000/record?id=audio_id&user=user_id


### Остановка и удаление контейнеров:
Чтобы остановить и удалить контейнеры, выполните следующую команду: <br>
docker-compose down

Все данные сохраняются в Docker volume, это означает, что данные сохраняются даже при остановке и удалении контейнеров. <br>
Если вам нужно удалить volume и все его данные, выполните следующую команду: <br>
docker volume rm your_repository_dbdata


*Made with Flask, Flask-SQLAlchemy and pydub
