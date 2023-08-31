# Django-подобный фреймворк (упрощенная версия)

## Присутствует и примесь от FastAPI такая как создание роутов декоратором AppRoute

1. Реализован основной рабочий файл запуска фреймворка: divo_framework/main.py
2. Реализована работа с шаблонами: divo_framework/templator.py
3. Реализована обработка GET и POST запросов от пользователя: divo_framework/framework_requests.py
4. Реализован запуск проекта через wsgi_static_middleware
5. Реализована возможность создания контроллеров на базе cbv: components/cbv.py
6. Реализован универсальный маппер для моделей (Student и Category как примеры): components/universal_mapper.py
