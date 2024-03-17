from fastapi import FastAPI
from fastapi import HTTPException
from my_langchain.model import HomeAssist
import uvicorn
from pydantic_models import PromptTemplate


app = FastAPI()
home_assist = HomeAssist()


@app.post("/ask")
async def ask_question(request_json: PromptTemplate):
    try:
        # Turn request_json into a Python dict
        prompt = request_json.dict()

        result = home_assist.ask_ai(prompt)
        print(result)
        return {"output": result}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8112)
