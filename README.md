# UGC_Service
ССЫЛКА НА РЕПОЗИТОРИЙ: https://github.com/mederunov/UGC_Service

# Запуск приложения
- Проверьте установлены все необходимое для запуска приложения
- Переименуте файл .env.example или скопируйте его содержимое в .env файл
- Замените значения логинов и паролей в переменных окружения
- Создайте сеть в докере:
```bash
    docker network create practicumAPI
```
- Запустите команду:

```bash
    docker-compose up --build -d
```

# Swagger UI 
Можно посмотреть по url: `/api/openapi#/`