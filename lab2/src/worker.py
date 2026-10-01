import os
from PyQt6.QtCore import QThread, pyqtSignal
from parser import parse_image

class ScannerThread(QThread):
    result_ready = pyqtSignal(dict)
    progress_update = pyqtSignal(int)

    def __init__(self, files):
        super().__init__()
        self.files = files

    def run(self):
        for i, filepath in enumerate(self.files):
            filename = os.path.basename(filepath)
            try:
                meta = parse_image(filepath)
                meta["filename"] = filename
                self.result_ready.emit(meta)
            except Exception:
                self.result_ready.emit({
                    "filename": filename,
                    "status": "Ошибка чтения"
                })
            self.progress_update.emit(i + 1)