from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

#Url local : http://127.0.0.1:8000

@app.get("/url")
async def get_url():
    return {"url_curso": "http://www.google.com"}

#Url local : http://127.0.0.1:8000/url
#Documentacion: http://127.0.0.1:8000/docs