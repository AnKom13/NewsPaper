import time
import datetime

def timing(get_response):
    def middleware(request):
        request.current_time = datetime.datetime.now()
        t1 = time.time()
        response = get_response(request)
        t2 = time.time()
        print("Время работы:", (t2 - t1))
        return response
    return middleware
