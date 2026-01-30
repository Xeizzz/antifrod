## Используемые технологии
- Python
- FastAPI
- Pydantic
- Redis
- Pytest
- Prometheus
- Grafana
- Docker / Docker Compose

Запуск локальный
```bash
uv run src/run.py
```


### Запуск
Из корня проекта выполните команду:
```bash
docker compose up --build
```
### Доступные адреса
- Swagger UI: http://localhost:8080/docs
- Метрики сервиса: http://localhost:8080/metrics
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

### Данные для входа в Grafana
- Логин: admin
- Пароль: admin


### Запуск всех тестов
```bash
pytest src/tests/ -v
```
