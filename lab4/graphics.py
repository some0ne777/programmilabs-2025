import matplotlib.pyplot as plt
import pandas as pd


def plot_histogram(df: pd.DataFrame):
    """Создание гистограммы распределения по диапазонам яркости."""
    counts = df['Категория_яркости'].value_counts()
    
    def get_min_val(category):
        return int(category.split('-')[0])
    
    categories = sorted(counts.index, key=get_min_val)
    values = [counts[cat] for cat in categories]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(categories, values, color='skyblue', edgecolor='black', width=0.7)

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom')
    
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    return fig


def save_results(sorted_df: pd.DataFrame, hist_fig):
    """Сохранение DataFrame и гистограммы."""
    if 'Bin_Number' in sorted_df.columns:
        output_df = sorted_df.drop(columns=['Bin_Number'])
    else:
        output_df = sorted_df.copy()
    
    output_df.to_csv('result.csv', index=False, encoding='utf-8')
    
    if hist_fig:
        hist_fig.savefig('grafik.png', dpi=300, bbox_inches='tight')
        plt.close(hist_fig)