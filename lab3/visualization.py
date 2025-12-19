import matplotlib.pyplot as plt


def display_images(
    original,
    result,
    original_title="Исходное изображение",
    result_title="Результат с рамкой",
    figsize=(15, 6),
):
    """Отображение изображений с использованием matplotlib"""

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

    ax1.imshow(original)
    ax1.set_title(original_title, fontsize=14, fontweight="bold")
    ax1.axis("off")

    orig_height, orig_width = original.shape[:2]
    ax1.text(
        0.5,
        -0.1,
        f"Размер: {orig_width}×{orig_height}",
        transform=ax1.transAxes,
        ha="center",
        fontsize=10,
    )

    ax2.imshow(result)
    ax2.set_title(result_title, fontsize=14, fontweight="bold")
    ax2.axis("off")

    result_height, result_width = result.shape[:2]
    ax2.text(
        0.5,
        -0.1,
        f"Размер: {result_width}×{result_height}",
        transform=ax2.transAxes,
        ha="center",
        fontsize=10,
    )

    plt.tight_layout()
    plt.show()