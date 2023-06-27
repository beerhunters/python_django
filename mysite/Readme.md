## Проект простого Интернет-магазина

### Инструкция по установке и первому запуску 

Установить зависимости:

```bash
pip install -r requirements.txt
```

Провести миграцию:

```bash
python manage.py makemigrations
python manage.py migrate
```

Загрузить тестовые данные:

```bash
python manage.py loaddata goods.csv
```

Создать суперпользователя:

```bash
python manage.py createsuperuser
```

Запустить веб-сервер проекта:

```bash
python manage.py runserver
```

## Примеры работы API
По умолчанию пагинация установлена на 2 записи
* [получение полного списка товаров](http://127.0.0.1:8000/ru/shop/api/products/)
* [получение списка заказов](http://127.0.0.1:8000/ru/shop/api/orders/)
* [получение списка товаров по названию или его части](http://127.0.0.1:8000/ru/shop/api/products/?name=Desktop)