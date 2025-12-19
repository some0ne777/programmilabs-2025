import cv2
import numpy as np
from PIL import Image


def get_border_color(color_name):
    """Получение цвета рамки в формате RGB"""
    colors = {
        "red": (255, 0, 0),
        "blue": (0, 0, 255),
        "green": (0, 255, 0),
        "black": (0, 0, 0),
        "white": (255, 255, 255),
    }

    return colors.get(color_name, colors["red"])


def get_image_size(image_path):
    """Получение размера изображения"""
    try:
        with Image.open(image_path) as img:
            return img.size
    except Exception as e:
        raise ValueError(f"Не удалось открыть изображение: {e}")


def load_image_opencv(image_path):
    """Загрузка изображения с использованием OpenCV"""
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Не удалось загрузить изображение: {image_path}")
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def save_image_opencv(image, output_path):
    """Сохранение изображения с использованием OpenCV"""
    image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    success = cv2.imwrite(output_path, image_bgr)
    if not success:
        raise ValueError(f"Не удалось сохранить изображение: {output_path}")
    return success