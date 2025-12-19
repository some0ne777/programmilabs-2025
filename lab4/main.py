import sys
from brightness_processing import *
from graphics import *


def main():
    if len(sys.argv) < 2:
        print("Запуск: python main.py annotation.csv")
        return
    csv_file = sys.argv[1]

    try:
        df = create_dataframe(csv_file)
        df = add_brightness_column(df)
        df = create_categories(df)
        sorted_df = sort_by_column(df, "Диапазон_яркости")
        hist = plot_histogram(df)
        save_results(sorted_df, hist)
        print("Файлы сохранены:")
        print("- result.csv")
        print("- grafik.png")

    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()