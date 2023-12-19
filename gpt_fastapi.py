from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from starlette.responses import HTMLResponse, RedirectResponse


class Settings:
    OPENAI_API_KEY: str = 'OPENAI_API_KEY'

    class Config:
        env_file = '.env'


class GPTRequest(BaseModel):
    modelName: str = "gpt-3.5-turbo-1106"
    temperature: float = 0
    systemPrompt: str = "Ты вежливый ИИ-ассистент."
    userPrompt: str = "Расскажи сказку про большую языковую модель"


settings = Settings()
client = OpenAI(api_key=settings.OPENAI_API_KEY)
app = FastAPI()


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url='/docs')


@app.post("/gpt", response_class=HTMLResponse)
def index(request: GPTRequest):
    response = client.chat.completions.create(
        model=request.modelName,
        temperature=request.temperature,
        messages=[{"role": "system",
                   "content": request.systemPrompt},
                  {"role": "user",
                   "content": request.userPrompt}]
    )
    result = response.choices[0].message.content
    return {"result": result}
