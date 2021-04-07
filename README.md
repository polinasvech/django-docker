# Printer API

Для создания чеков передите на 
http://localhost:8000/create_checks/

Для получения списка новых чеков перейдите на 
http://localhost:8000/new_checks/?api_key=<printer_api_key>/

Для получения PDF-файла чека перейдите на http://localhost:8000/check/?api_key=<priner_api_key>&check_id=<check_id>/

--------------------------------------------------------
Для просмотра всех чеков перейдите на http://localhost:8000/admin/checkservice/check/

Для просмотра всех принтеров http://localhost:8000/admin/checkservice/printer/

Для входа использовать данные пользователя, созданного на шаге 4.

-------------------------------------------
Для отслеживания работы воркера перейдите на http://localhost:8000/admin/rq/
___________________________________________
**Порядок запуска**
1. Устанавливаем зависимости
```
pip install -r requirements.txt
```
2. В фоновом режиме запускаем необходимые для работы сервисы
```
docker-compose up -d
```
3. Создаем и прогоняем миграции
```
python manage.py makemigrations
python manage.py migrate
```
4. Создаем пользователя для доступа в административный раздел
```
python manage.py createsuperuser
```
5. Загружаем начальные данные для таблицы принтеров
```
python manage.py loaddata printer_data.json
```
6. Запускаем воркер
```
python manage.py rqworker
```
7. Запускаем сервер
```
python manage.py runserver
```