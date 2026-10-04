 

# Backend: Plan

## Запуск

```bash
docker compose up -d --build
docker compose exec backend python manage.py init_bd
```

init_bd - создает группы, два ЗМК и трех пользователей


- Swagger: http://localhost:8000/api/docs/
- Схема OpenAPI: http://localhost:8000/api/schema/


## Тестовый запрос
тестовые запросы можно отправлять через Swagger
открываем нужный маршрут, подставляем json, отправляем запрос.  
будет результат.

```json
POST /work-volume-list/
{"factory": 1, "start": "2026-10-02", "finish": "2026-10-08", "weight": 1000, "author": 1}
```

#коды
 201 - все ок 
 403 - отказ в доступе 
 404 - `-errorCode=174`: ЗМК не существует или пользователь не относится к ЗМК 
 406 - `errorCode=279`: не заполнены обязательные поля 


