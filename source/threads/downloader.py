import logging
from dataclasses import dataclass
from pathlib import Path

from modules._copyfileobj import copyfileobj
from modules.connection_manager import REQUEST_MANAGER
from modules.enums import MessageType
from modules.settings import get_library_folder
from modules.task import Task
from PyQt5.QtCore import pyqtSignal
from urllib3.exceptions import MaxRetryError


@dataclass(frozen=True)
class DownloadTask(Task):
    manager: REQUEST_MANAGER
    link: str
    progress = pyqtSignal(int, int)
    finished = pyqtSignal(Path)

    def run(self):
        self.progress.emit(0, 0)
        temp_folder = Path(get_library_folder()) / ".temp"
        temp_folder.mkdir(exist_ok=True)
        dist = temp_folder / Path(self.link).name

        try:
            with self.manager.request("GET", self.link, preload_content=False, timeout=10) as r:
                self._download(r, dist)
        except MaxRetryError as e:
            logging.error(e)
            self.message.emit("Requesting is taking longer than usual! see debug logs for more.", MessageType.ERROR)
            with self.manager.request("GET", self.link, preload_content=False) as r:
                self._download(r, dist)

        self.finished.emit(dist)

    def _download(self, r, dist: Path):
        size = int(r.headers["Content-Length"])
        with dist.open("wb") as f:
            copyfileobj(r, f, lambda x: self.progress.emit(x, size))

    def __str__(self):
        return f"Download {self.link}"
