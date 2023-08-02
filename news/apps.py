from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'
    # print ('Конфиг загружен.')

    def ready(self):
        import news.signals
