import argparse

def parse_arguments():
    """Парсинг аргументов командной строки"""
    parser = argparse.ArgumentParser(
        description='Обработка изображения с наложением рамки'
    )
    
    parser.add_argument('input_path', type=str, help='Путь к исходному файлу изображения')
    parser.add_argument('output_path', type=str, help='Путь для сохранения результата')
    parser.add_argument('--border_width', type=int, default=20, 
                       help='Ширина рамки в пикселях (по умолчанию: 20)')
    parser.add_argument('--border_color', type=str, default='red', 
                       choices=['red', 'blue', 'green', 'black', 'white'],
                       help='Цвет рамки (по умолчанию: red)')
    
    return parser.parse_args()

def validate_arguments(args):
    """Валидация аргументов"""
    if args.border_width < 0:
        raise ValueError("Ширина рамки не может быть отрицательной")
    
    return args