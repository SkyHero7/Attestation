from django.apps import AppConfig


class NetworkConfig(AppConfig):
    """
    Конфигурация приложения сети.

    Атрибуты:
        default_auto_field (str): Поле по умолчанию для автоинкрементных идентификаторов.
        name (str): Имя приложения в проекте Django.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'network'
