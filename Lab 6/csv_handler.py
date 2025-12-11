import os
import logging
from functools import wraps

class FileNotFound(Exception):
    pass

class FileCorrupted(Exception):
    pass

def logged(exception_type, mode="console"):
    logger = logging.getLogger("file_logger")
    logger.setLevel(logging.ERROR)
    if logger.hasHandlers():
        logger.handlers.clear()
    if mode == "console":
        handler = logging.StreamHandler()
    elif mode == "file":
        handler = logging.FileHandler("log.txt", mode="a", encoding="utf-8")
    else:
        raise ValueError("mode must be 'console' or 'file'")
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exception_type as e:
                logger.error(f"{func.__name__}: {str(e)}")
                raise
        return wrapper
    return decorator

class CSVFileHandler:
    @logged(FileNotFound, mode="console")
    def __init__(self, filepath):
        self.filepath = filepath
        if not os.path.exists(filepath):
            raise FileNotFound(f"Файл '{filepath}' не знайдено")

    @logged(FileCorrupted, mode="file")
    def read(self):
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
            return [line.split(",") for line in lines if line]
        except Exception:
            raise FileCorrupted("Не вдалося прочитати файл")

    @logged(FileCorrupted, mode="file")
    def write(self, rows):
        try:
            rows.sort(key=lambda x: x[0].lower())
            with open(self.filepath, "w", encoding="utf-8") as f:
                for row in rows:
                    f.write(",".join(map(str, row)) + "\n")
        except Exception:
            raise FileCorrupted("Не вдалося записати у файл")

    @logged(FileCorrupted, mode="file")
    def append(self, rows):
        try:
            data = self.read()
            data.extend(rows)
            self.write(data)
        except Exception:
            raise FileCorrupted("Не вдалося дописати у файл")
