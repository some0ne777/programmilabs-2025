import csv
import os
from typing import Iterator, List


class ImagePathIterator:
    """Итератор путей файлов"""

    def __init__(self, source_path: str) -> None:
        if not isinstance(source_path, str):
            raise ValueError("source_path must be a string")

        self.source_path = source_path
        self.use_annotation = source_path.endswith(".csv")
        self.image_paths: List[str] = []
        self._load_paths()

    def _load_paths(self) -> None:
        """Загружает пути к изображениям из файла с аннотацией или папки"""
        if self.use_annotation:
            try:
                with open(self.source_path, "r", encoding="utf-8") as csvfile:
                    reader = csv.DictReader(csvfile, delimiter=";")
                    for row in reader:
                        file_path = row.get("Absolute_path", "").strip()
                        if file_path and os.path.exists(file_path):
                            self.image_paths.append(file_path)
            except (FileNotFoundError, KeyError) as e:
                raise ValueError(f"Ошибка загрузки CSV: {e}")
        else:
            if not (
                os.path.exists(self.source_path) and os.path.isdir(self.source_path)
            ):
                raise ValueError(f"Папка не существует: {self.source_path}")

            image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
            for root, _, files in os.walk(self.source_path):
                for file in files:
                    file_extension = os.path.splitext(file)[1].lower()
                    if file_extension in image_extensions:
                        file_path = os.path.join(root, file)
                        if os.path.isfile(file_path):
                            abs_path = os.path.abspath(file_path)
                            self.image_paths.append(abs_path)

    def __iter__(self) -> Iterator[str]:
        """Возвращает итератор."""
        self._current_index = 0
        return self

    def __next__(self) -> str:
        """Возвращает следующий путь к изображению."""
        if self._current_index < len(self.image_paths):
            path = self.image_paths[self._current_index]
            self._current_index += 1
            return path
        raise StopIteration

    def __len__(self) -> int:
        """Возвращает количество путей"""
        return len(self.image_paths)

    def __getitem__(self, index: int) -> str:
        """Получение пути по индексу"""
        return self.image_paths[index]