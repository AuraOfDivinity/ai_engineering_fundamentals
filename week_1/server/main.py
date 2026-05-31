import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

# load the environment variables from the dot env files
load_dotenv()

# init fats api app
app = FastAPI()

# init openai client. This automatically chesks for the OPENAI_API_KEY aev variable
client = OpenAI()

# Define the structure for the user message
class UserMessage(BaseModel):
    prompt: str

@app.get('/healthcheck')
async def healthcheck():
    try:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if(openai_api_key):
            return { "status": "healthy"}
        else:
            raise HTTPException(status_code=503, detail="Service Unavailable")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/chat')
async def ask_ai(message: UserMessage):
    try:
        # Call chat completion api
        response = client.chat.completions.create(
            model="gpt-5.4-mini", # Or your preferred available model
            messages=[
                {"role": "system", "content": "You are a helpful assistant running on a local FastAPI server."},
                {"role": "user", "content": message.prompt}
            ]
        )
        # Extract the text answer out of the response object
        ai_answer = response.choices[0].message.content
        return {"response": ai_answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

