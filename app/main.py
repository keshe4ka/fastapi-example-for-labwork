import uvicorn
from fastapi import FastAPI

from app.modules.users.views import router as user_router
from app.modules.computers.views import router as computer_router

app = FastAPI()

app.include_router(user_router)
app.include_router(computer_router)


@app.get('/')
def root():
    return {
        'name': 'Lab9',
        'version': '1.0.0',
        'swagger': '/docs'
    }


if __name__ == '__main__':
    uvicorn.run('main:app', port=8080, host='0.0.0.0', reload=True)
