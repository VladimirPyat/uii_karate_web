from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi import Request
from fastapi.templating import Jinja2Templates

import uvicorn
import os

from models.fake_model import FakeModel
from utils.file_utils import FileReader
from views.html_view import HtmlView

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# создаем экземпляры моделей
file_reader = FileReader()
view = HtmlView()
model = FakeModel()           #для демонстрации работы приложения
KATA_NAMES = model.get_kata()

# хранение загруженных видео
UPLOAD_DIRECTORY = "_uploads"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


# КОНЕЧНЫЕ ТОЧКИ

@app.exception_handler(HTTPException)
async def custom_exception_handler(request: Request, exc: HTTPException):
    print('error')
    return view.error_page(request, {
        "message": str(exc),
        "url": "/"
    }, status_code=400)


@app.get("/")
async def main_view(request: Request):
    return view.upload_page(request, {})


# загрузка видео
@app.post("/upload-video/")
async def upload_video(request: Request, file: UploadFile = File(...)):
    # проверяем является ли расширение допустимым
    if not file_reader.is_allowed_file(file.filename):
        return view.upload_page(request, content={"message": "Формат файла не поддерживается", },
                                status_code=400)
    try:
        await file_reader.upload_file(UPLOAD_DIRECTORY, file)
        # Возвращаем ссылку на загруженное видео
        video_path = f"/{UPLOAD_DIRECTORY}/{file.filename}"
        return view.upload_page(request, content={"message": f"Видео загружено {file.filename}",
                                                  "selector": KATA_NAMES,
                                                  "file_path": video_path},
                                status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# обработка видео
@app.get("/process-video/")
async def process_video(request: Request):
    file_path = request.query_params.get("file_path")
    kata_name = request.query_params.get("kata_name")
    kata_results = model.process(kata_name, file_path)
    return view.process_page(request, content={"message": "",
                                               "kata_name": kata_name,
                                               "kata_results": kata_results},
                             status_code=200)


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
