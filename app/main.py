from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

app = FastAPI()

# Static 파일을 위해 마운트 설정
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root(request: Request):
    analysis_result = "60%"  # 예시 결과
    return templates.TemplateResponse("index.html", {"request": request, "analysis_result": analysis_result})
