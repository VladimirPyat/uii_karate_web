import os


class FileReader:
    """
    класс для работы с файлами: чтение, запись
    """
    VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mov', '.mkv'}
    path = None

    def is_allowed_file(self, file_name):
        ext = os.path.splitext(file_name)[1].lower()
        allowed = ext in self.VIDEO_EXTENSIONS

        return allowed

    async def upload_file(self, file_dir, file):
        # запись файла по ссылке
        self.path = os.path.join(file_dir, file.filename)
        with open(self.path, "wb") as f:
            f.write(await file.read())
