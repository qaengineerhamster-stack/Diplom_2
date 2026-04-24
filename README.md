# Diplom_2

## API-автотесты для Stellar Burgers

Использованы:
- pytest
- requests
- allure-pytest

### Покрытые сценарии

- создание пользователя
- логин пользователя
- создание заказа
- позитивные и негативные сценарии

### Структура проекта

- `helpers.py` — логические методы для работы с API
- `data.py` — тестовые данные и ожидаемые сообщения
- `tests/` — API-тесты
- `tests/conftest.py` — фикстуры с предусловиями и постусловиями

### Запуск тестов

```bash
pip install -r requirements.txt
pytest
```

### Запуск с Allure

```bash
pytest --alluredir=allure_results
```
