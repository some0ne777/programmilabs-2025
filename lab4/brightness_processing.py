import os
import pandas as pd
from PIL import Image
import numpy as np


def create_dataframe(csv_file: str) -> pd.DataFrame:
    """Создание DataFrame с двумя колонками путей."""
    df = pd.read_csv(csv_file, encoding='utf-8', sep=';')
    
    if 'Absolute_path' not in df.columns or 'Relative_path' not in df.columns:
        raise ValueError("CSV должен содержать  'Absolute_path' и 'Relative_path'")
    
    result = pd.DataFrame({
        'Абсолютный_путь': df['Absolute_path'],
        'Относительный_путь': df['Relative_path']
    })
    
    return result


def add_brightness_column(df: pd.DataFrame) -> pd.DataFrame:
    """Добавление колонки с диапазоном яркости (max-min)."""
    brightness_ranges = []
    
    for path in df['Абсолютный_путь']:
        try:
            with Image.open(path) as img:
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                arr = np.array(img)

                brightness_range = float(np.max(arr) - np.min(arr))
                brightness_ranges.append(brightness_range)
                
        except Exception as e:
            print(f"Ошибка при обработке {path}: {e}")
            brightness_ranges.append(0.0)
    
    df['Диапазон_яркости'] = brightness_ranges
    return df


def create_categories(df: pd.DataFrame, num_bins: int = 5) -> pd.DataFrame:
    """Создание категорий (диапазонов) для гистограммы."""
    min_val = df['Диапазон_яркости'].min()
    max_val = df['Диапазон_яркости'].max()
    
    edges = np.linspace(min_val, max_val, num_bins + 1)
    
    categories = []
    bin_numbers = []
    
    for val in df['Диапазон_яркости']:
        for i in range(num_bins):
            if edges[i] <= val < edges[i + 1]:
                if i == num_bins - 1:
                    categories.append(f"{int(edges[i])}-{int(edges[i + 1])}")
                else:
                    categories.append(f"{int(edges[i])}-{int(edges[i + 1])}")
                bin_numbers.append(i)
                break
        else:
            categories.append(f"{int(edges[-2])}-{int(edges[-1])}")
            bin_numbers.append(num_bins - 1)
    
    df['Категория_яркости'] = categories
    df['Bin_Number'] = bin_numbers
    return df


def sort_by_column(df: pd.DataFrame, column: str, ascending: bool = True) -> pd.DataFrame:
    """Сортировка по указанной колонке."""
    return df.sort_values(column, ascending=ascending).reset_index(drop=True)


def filter_by_column(df: pd.DataFrame, column: str, min_val=None, max_val=None) -> pd.DataFrame:
    """Фильтрация по указанной колонке."""
    result = df.copy()
    if min_val is not None:
        result = result[result[column] >= min_val]
    if max_val is not None:
        result = result[result[column] <= max_val]
    return result.reset_index(drop=True)