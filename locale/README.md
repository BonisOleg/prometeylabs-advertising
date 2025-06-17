# Локалізація

Ця директорія містить файли перекладів для підтримки мультимовності.

## Структура:
- `uk/` - українська мова (основна)
- `en/` - англійська мова
- `ru/` - російська мова (за потребою)

## Генерація файлів перекладу:
```bash
python manage.py makemessages -l uk
python manage.py makemessages -l en
python manage.py compilemessages
```

## Використання в шаблонах:
```html
{% load i18n %}
{% trans "Текст для перекладу" %}
```

## Використання в коді:
```python
from django.utils.translation import gettext as _
message = _("Повідомлення для перекладу")
``` 