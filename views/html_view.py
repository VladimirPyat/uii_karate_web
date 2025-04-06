from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

templates = Jinja2Templates(directory="templates")


class HtmlView:
    @staticmethod
    def upload_page(request: Request, content : dict, status_code: int = 200):
        return templates.TemplateResponse("uploads.html", {
            "request": request,
            "message": content.get("message", ''),
            "selector": content.get("selector", ''),
            "file_path": content.get("file_path", '')

        }, status_code=status_code)

    @staticmethod
    def process_page(request: Request, content: dict, status_code: int = 200):
        return templates.TemplateResponse("video_proc.html", {
            "request": request,
            "kata_name": content.get("kata_name", ''),
            "kata_results": content.get("kata_results", '')

        }, status_code=status_code)

    @staticmethod
    def error_page(request: Request, content: dict, status_code: int = 400):
        return templates.TemplateResponse("errors.html", {
            "request": request,
            "message": content.get("message", "Произошла ошибка"),
            "back_url": content.get("url", "/"),
        }, status_code=status_code)