import cv2
import numpy as np
from PIL import Image
from image_utils import get_border_color, load_image_opencv


class BorderProcessor:
    """Класс для обработки изображений с добавлением рамки"""

    def __init__(self, border_width, border_color_name):
        self.border_width = border_width
        self.border_color = get_border_color(border_color_name)

    def add_border(self, image_path):
        """Добавление рамки с использованием OpenCV"""
        img = load_image_opencv(image_path)
        height, width = img.shape[:2]

        bordered_img = cv2.copyMakeBorder(
            img,
            self.border_width,
            self.border_width,
            self.border_width,
            self.border_width,
            cv2.BORDER_CONSTANT,
            value=self.border_color,
        )

        return img, bordered_img

    def get_processing_info(self):
        """Получение информации о параметрах обработки"""
        return {
            "border_width": self.border_width,
            "border_color": self.border_color,
        }

    def get_original_image_size(self, image_path):
        """Получение размера исходного изображения"""
        with Image.open(image_path) as img:
            return img.size