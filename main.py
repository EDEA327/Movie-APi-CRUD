from fastapi import FastAPI

app = FastAPI(title='My Movie App', version='0.0.1', description='Una api de introducción a Fast API')


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello {name}"}
