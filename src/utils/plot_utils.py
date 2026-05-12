import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def save_professional_plot(fig, filename: Path, dpi: int = 120):
    """
    Save a matplotlib figure with StreamIQ's professional sizing standards.
    - figsize: (5,4)
    - font_scale: 0.9
    - dpi: 120 (default)
    """
    sns.set(font_scale=0.9)
    fig.set_size_inches(5, 4)
    fig.tight_layout()
    fig.savefig(filename, dpi=dpi)
    print(f"📊 Professional plot saved to {filename}")
