import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from arg_parser import parse_arguments, validate_arguments
from border_processor import BorderProcessor
from visualization import display_images
from image_utils import save_image_opencv


def main():
    try:
        args = parse_arguments()
        args = validate_arguments(args)

        processor = BorderProcessor(
            border_width=args.border_width, border_color_name=args.border_color
        )

        original_size = processor.get_original_image_size(args.input_path)
        original_image, result_image = processor.add_border(args.input_path)

        print("=" * 50)
        print(f"Исходный размер: {original_size[0]}×{original_size[1]} пикселей")
        print(f"Ширина рамки: {args.border_width} пикселей")
        print(f"Цвет рамки: {args.border_color}")
        print("=" * 50 + "\n")

        display_images(
            original_image,
            result_image,
            original_title=f"Исходное изображение\n{original_size[0]}×{original_size[1]}",
            result_title=f"С рамкой {args.border_color}",
        )

        save_image_opencv(result_image, args.output_path)

    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()