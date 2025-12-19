import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication, QFileDialog, QHBoxLayout, QLabel, QMainWindow,
    QPushButton, QVBoxLayout, QWidget
)

from dataset_iterator import ImagePathIterator


class ImageViewer(QMainWindow):
    def __init__(self) -> None:
        """Инициализирует окно просмотра изображений."""
        super().__init__()
        self.iterator = None
        self.current_index = 0

        self.setWindowTitle("Просмотр изображений")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        self.image_label = QLabel("Выберите файл или папку")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(400, 300)
        main_layout.addWidget(self.image_label)

        button_layout = QHBoxLayout()

        csv_button = QPushButton("CSV файл")
        csv_button.clicked.connect(self.load_csv)
        button_layout.addWidget(csv_button)

        dir_button = QPushButton("Папка")
        dir_button.clicked.connect(self.load_dir)
        button_layout.addWidget(dir_button)

        self.prev_button = QPushButton("Назад")
        self.prev_button.clicked.connect(self.show_prev)
        self.prev_button.setEnabled(False)
        button_layout.addWidget(self.prev_button)

        self.next_button = QPushButton("Вперед")
        self.next_button.clicked.connect(self.show_next)
        self.next_button.setEnabled(False)
        button_layout.addWidget(self.next_button)

        main_layout.addLayout(button_layout)

    def load_csv(self) -> None:
        """Загружает изображения из CSV файла."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите CSV файл", "", "CSV файлы (*.csv);;Все файлы (*)"
        )
        if file_path:
            self._load_source(file_path)

    def load_dir(self) -> None:
        """Загружает изображения из указанной директории."""
        dir_path = QFileDialog.getExistingDirectory(
            self, "Выберите папку с изображениями"
        )
        if dir_path:
            self._load_source(dir_path)

    def _load_source(self, source_path: str) -> None:
        """Загружает источник данных."""
        try:
            self.iterator = ImagePathIterator(source_path)
            self.current_index = 0
            self._update_navigation()
            self._show_current_image()
        except Exception as e:
            self.image_label.setText(f"Ошибка: {str(e)}")

    def _show_current_image(self) -> None:
        """Отображает текущее изображение."""
        if not self.iterator or self.current_index >= len(self.iterator):
            return

        try:
            image_path = self.iterator[self.current_index]
            pixmap = QPixmap(image_path)

            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(
                    self.image_label.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation,
                )
                self.image_label.setPixmap(scaled_pixmap)
            else:
                self.image_label.setText("Невозможно загрузить изображение")
        except Exception:
            self.image_label.setText("Ошибка загрузки изображения")

    def show_next(self) -> None:
        """Переходит к следующему изображению."""
        if self.iterator and self.current_index < len(self.iterator) - 1:
            self.current_index += 1
            self._update_navigation()
            self._show_current_image()

    def show_prev(self) -> None:
        """Возвращается к предыдущему изображению."""
        if self.iterator and self.current_index > 0:
            self.current_index -= 1
            self._update_navigation()
            self._show_current_image()

    def _update_navigation(self) -> None:
        """Обновляет состояние кнопок навигации."""
        if self.iterator:
            self.prev_button.setEnabled(self.current_index > 0)
            self.next_button.setEnabled(
                self.current_index < len(self.iterator) - 1
            )

    def resizeEvent(self, event):
        """Перерисовывает изображение при изменении размера окна."""
        super().resizeEvent(event)
        if self.iterator and len(self.iterator) > 0:
            self._show_current_image()


def main() -> None:
    """вход в приложение."""
    app = QApplication(sys.argv)
    window = ImageViewer()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()