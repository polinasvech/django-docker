# Printer API

Для создания чеков передите на 
http://localhost:8000/create_checks/

Для получения списка новых чеков перейдите на 
http://localhost:8000/new_checks/?api_key=<printer_api_key>

Для получения PDF-файла чека перейдите на http://localhost:8000:8000/check/?api_key=<priner_api_key>&check_id=<check_id>

Для просмотра всех чеков перейдите на http://localhost:8000/admin/checkservice/check/

Для просмотра всех принтеров http://localhost:8000/admin/checkservice/printer/

Для отслеживания работы воркера перейдите на http://localhost:8000/admin/rq/