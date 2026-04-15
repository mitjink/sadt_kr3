# Контрольная работа 3

**Технологии разработки серверных приложений**  
**Студент:** Доськова Мария Павловна  
**Группа:** ЭФБО-03-24  
**Семестр:** 4 семестр, 2025/2026 уч. год

## Инструкция по запуску
1. Клонировать репозиторий:

git clone https://github.com/mitjink/sadt_kr3  

2. Создать и активировать виртуальное окружение:

### Windows
python -m venv venv  
venv\Scripts\activate

### Mac/Linux
python3 -m venv venv  
source venv/bin/activate


3. Установить зависимости  
pip install -r requirements.txt  

4. Запуск приложений  

### Задание 6.1  
uvicorn task_6_1:app --reload --port 8001  

### Задание 6.2  
uvicorn task_6_2:app --reload --port 8002  

### Задание 6.3  
uvicorn task_6_3:app --reload --port 8003  

### Задание 6.4  
uvicorn task_6_4:app --reload --port 8004  

### Задание 6.5  
uvicorn task_6_5:app --reload --port 8005  

### Задание 7.1  
uvicorn task_7_1:app --reload --port 8006

### Задание 8.1  
uvicorn task_8_1:app --reload --port 8007  

### Задание 8.2  
uvicorn task_8_2:app --reload --port 8008  

## Тестирование ключевых эндпоинтов (curl)

### Задание 6.1  
Успешный вход  
curl -u user1:password1 http://localhost:8001/login  

Неверный пароль  
curl -u user1:wrong_password http://localhost:8001/login  

Без аутентификации  
curl http://localhost:8001/login  

### Задание 6.2  
Регистрация  
curl -X POST http://localhost:8002/register \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "12345"}'

Логин  
curl -u user:12345 http://localhost:8002/login  

### Задание 6.3  
Доступ к документации  
curl -u admin:secret http://localhost:8003/docs  

Проверка режима работы  
curl http://localhost:8003/  
### Задание 6.4  
Получить токен  
curl -X POST http://localhost:8004/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "adminpass"}'  

Использовать токен (TOKEN подставить из ответа)  
curl -H "Authorization: Bearer <TOKEN>" http://localhost:8004/protected_resource  
### Задание 6.5  
Регистрация (1 запрос в минуту)  
curl -X POST http://localhost:8005/register \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "qwerty123"}'

Логин (5 запросов в минуту)  
curl -X POST http://localhost:8005/login \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "qwerty123"}'

Доступ к защищённому ресурсу  
curl -H "Authorization: Bearer <TOKEN>" http://localhost:8005/protected_resource
### Задание 7.1  
Получить токен для admin  
curl -X POST http://localhost:8006/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "adminpass"}'

Создать ресурс (только admin)  
curl -X POST http://localhost:8006/resources \
  -H "Authorization: Bearer <TOKEN_ADMIN>" \
  -H "Content-Type: application/json" \
  -d '{"title": "New Resource"}'

Получить ресурсы (admin и user)  
curl -H "Authorization: Bearer <TOKEN>" http://localhost:8006/resources

Защищённый ресурс (только admin и user)  
curl -H "Authorization: Bearer <TOKEN>" http://localhost:8006/protected_resource
### Задание 8.1  
Регистрация
curl -X POST http://localhost:8007/register \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "12345"}'

Получить всех пользователей
curl http://localhost:8007/users

Получить пользователя по ID
curl http://localhost:8007/users/1
### Задание 8.2  
Создать задачу (CREATE)  
curl -X POST http://localhost:8008/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Task 1", "description": "To, do, task"}'

Получить все задачи (READ ALL)  
curl http://localhost:8008/todos

Получить задачу по ID (READ)  
curl http://localhost:8008/todos/1

Обновить задачу (UPDATE)  
curl -X PUT http://localhost:8008/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

Удалить задачу (DELETE)  
curl -X DELETE http://localhost:8008/todos/1