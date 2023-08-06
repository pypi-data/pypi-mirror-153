import datetime
import time

from aiohttp.web_exceptions import HTTPException
from jija.middleware import Middleware


class PrintRequest(Middleware):
    async def handler(self, request, handler):
        timer = time.time()
        try:
            response = await handler(request)

        except HTTPException as exception:
            PrintRequest.print(timer, exception.status, request.url, request.method)
            raise exception

        except Exception as exception:
            PrintRequest.print(timer, 500, request.url, request.method)
            raise exception

        PrintRequest.print(timer, response.status, request.url, request.method)
        return response

    @classmethod
    def print(cls, timer, status, url, method):
        timer = time.time() - timer
        time_label = f'{datetime.datetime.today().replace(microsecond=0)}'
        print(f'[{time_label}] [{round(timer, 4)} s] [{status}] [{method}] {str(url).split("?")[0]}')
