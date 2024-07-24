import uvicorn
from fastapi import FastAPI

from vmrec.faiss import FAISS
from vmrec.agent import TinyAgent
from vmrec.utils import yaml_load
from vmrec.schema import Query

config = yaml_load(dir='./config.yaml')

faiss_storing = FAISS(config=config['faiss_settings'], 
                      data_dir='./vm_info.csv')

llm = TinyAgent(config=config['chat_model'])
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello!"}

@app.post("/query")
async def root(query: Query):
    context = faiss_storing.query(input=query.prompt)

    # context's type is pd.DataFrame, convert it into str
    addtional_info = ""
    for _, row in context.iterrows():
        addtional_info += row.text + "\n"

    result = llm.query(input=query, 
                       context=context)    
    
    # Extract information from the result
    result = result.split("<|assistant|>")[-1]

    return {"message": f"{result}"}

if __name__ == "__main__":
    uvicorn.run("main:app", 
                port=8000, 
                log_level="info", 
                reload=True)