# fastAPI_shop Project

# Super Fast API Shop 🚀

Минималистичный и высокопроизводительный интернет-магазин на FastAPI.  
Проект создан для демонстрации FASTAPI с использованием современных технологий.

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python)](https://www.python.org/)

## Особенности ✨
- Регистрация и аутентификация пользователей (JWT)
- Управление товарами (CRUD)
- Корзина покупок и оформление заказов
- Документация API через Swagger/Redoc
- Конфигурация через переменные окружения
- Поддержка PostgreSQL (через SQLAlchemy)
- Тесты с pytest

## Быстрый старт 🚀

### Предварительные требования
- Python 3.9+
- PostgreSQL
- Poetry (для управления зависимостями)

### Установка
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/IngvarOrlov/super-fast-API-shop.git
   cd super-fast-API-shop

2. Установите зависимости:
    ```bash
    poetry install
    
3. Создайте файл .env в корне проекта:
    ```bash
    DATABASE_URL=postgresql://user:password@localhost:5432/fast_shop
    SECRET_KEY=your-secret-key
    DEBUG=False

4. Запустите сервер:
    ```bash
    uvicorn app.main:app --reload

5. Откройте документацию API:
    ```bash
    Swagger: http://localhost:8000/docs

    Redoc: http://localhost:8000/redoc   