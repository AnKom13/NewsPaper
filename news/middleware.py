import time
import datetime

# def timing(get_response):
#     def middleware(request):
#         request.current_time = datetime.datetime.now()
#         t1 = time.time()
#         response = get_response(request)
#         t2 = time.time()
#         print("Время работы:", (t2 - t1))
#         return response
#     return middleware

import pytz

from django.utils import timezone


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tzname = request.session.get('django_timezone')  # пытаемся забрать часовой пояс из сессии
        #  если он есть в сессии, то выставляем такой часовой пояс. Если же его нет, значит он не установлен,
        #  и часовой пояс надо выставить по умолчанию (на время сервера)
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
        return self.get_response(request)
