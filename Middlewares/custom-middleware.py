import time
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

class TimerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start_time
        print(f'Request: {request.url.path} processed in {duration:.2f} seconds')
        return response

app.add_middleware(TimerMiddleware)

@app.get('/hello')
def hello():
    for _ in range(1000000):
        pass
    return {'message': 'Hello world'}
        