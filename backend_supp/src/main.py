import uvicorn
from fastapi import FastAPI, Request
from src.router import router

app = FastAPI()
origins = ['*']
app.include_router(router)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Request: {request.method} {request.url}", flush=True)
    response = await call_next(request)
    return response


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)