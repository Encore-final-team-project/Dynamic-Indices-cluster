from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
def read_root(request: Request):
    # 예제 데이터
    analysis_result = "애플의 망할 확률은 5%입니다."

    return templates.TemplateResponse("index.html", {"request": request, "analysis_result": analysis_result})
