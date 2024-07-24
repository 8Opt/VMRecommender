from fastapi import FastAPI

from vmrec.utils import yaml_load


config = yaml_load(dir='./config.yaml')

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello!"}
