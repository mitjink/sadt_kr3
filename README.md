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

