from fastapi import FastAPI
import app.Routers.Chatbot as Chatbot
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import os
import openai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(Chatbot.router, tags=["Chatbot"])

@app.get("/")
async def root():
    return {"message": "Hello World"}

###########################################################

@app.get("/headline-analysis/")
async def headline_analysis(stockName: str, headlineInfo: str):

    return_data = {
        "stockName": stockName,
        "headlineInfo": headlineInfo
    }

    api_key = os.getenv('OPENAI_API_KEY')
    MODEL = "gpt-4"
    prompt1 = """
You're an investor. I'll give you a headline from a company ${stockName}. You just answer is this news positive or negative or neutral for the price of the stock as a one word. choices: Positive, Negative, Neutral.
            """
    prompt2 = """
Here is a headline from a company ${stockName}. Would an investor consider this news more positive or more negative for the price of the stock. Explain in detail. 60 words
            """
    
    response = openai.ChatCompletion.create(
        model = MODEL,
        messages=[
            {"role": "system", "content": prompt1},
            {"role": "user", "content": return_data["headlineInfo"]}
        ],
        temperature=0,
    )

    return_data["status"] = response['choices'][0]['message']['content']
    
    response = openai.ChatCompletion.create(
        model = MODEL,
        messages=[
            {"role": "system", "content": prompt2},
            {"role": "user", "content": return_data["headlineInfo"]}
        ],
        temperature=0,
    )

    return_data["detail"] = response['choices'][0]['message']['content']
    
    return return_data

###########################################################


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7000, reload=True)
