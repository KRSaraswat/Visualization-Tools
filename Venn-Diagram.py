import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

def plot_venn3(set1, set2, set3, labels=None, colors=None, save_path=None, dpi=600, bold_labels=True):
    """
    Plots a 3-set Venn diagram manually, showing all 7 regions with accurate content placement.

    Args:
        set1, set2, set3: Python sets representing the three groups.
        labels: List of 3 strings, labels for each set. Defaults to ['Set 1', 'Set 2', 'Set 3'].
        colors: List of 3 hex color codes. Defaults to ['#E41A1C', '#377EB8', '#FFAB52'].
        save_path: If provided, saves the figure to this file path.
        dpi: Resolution of saved figure.
        bold_labels: Whether to show set labels in bold in their respective regions.
    """
    
    if labels is None:
        labels = ['Set 1', 'Set 2', 'Set 3']
    if colors is None:
        colors = ['#E41A1C', '#377EB8', '#FFAB52']
        
    sets = [set1, set2, set3]

    fig, ax = plt.subplots(figsize=(8, 8))

    sizes = [len(s) for s in sets]
    max_size = max(sizes)
    radii = [0.18 + 0.08 * (size / max_size) for size in sizes]

    def get_positions_with_overlap(radii, overlap_factor=0.6):
        d12 = (radii[0] + radii[1]) * overlap_factor
        d13 = (radii[0] + radii[2]) * overlap_factor
        d23 = (radii[1] + radii[2]) * overlap_factor

        x1, y1 = 0.5, 0.5
        x2, y2 = x1 + d12, y1

        angle = math.acos((d12**2 + d13**2 - d23**2) / (2 * d12 * d13))
        x3 = x1 + d13 * math.cos(angle)
        y3 = y1 + d13 * math.sin(angle)

        return [(x1, y1), (x2, y2), (x3, y3)]

    positions = get_positions_with_overlap(radii)

    for i, (pos, rad, color) in enumerate(zip(positions, radii, colors)):
        circle = patches.Circle(pos, radius=rad, facecolor=color, alpha=0.4, edgecolor='black', linewidth=1)
        ax.add_patch(circle)

    A, B, C = set1, set2, set3

    only_A   = A - B - C
    only_B   = B - A - C
    only_C   = C - A - B
    A_B      = (A & B) - C
    A_C      = (A & C) - B
    B_C      = (B & C) - A
    A_B_C    = A & B & C

    region_texts = [
        (only_A,   (positions[0][0] - 0.07, positions[0][1] - 0.05)),
        (only_B,   (positions[1][0] + 0.07, positions[1][1] - 0.05)),
        (only_C,   (positions[2][0],        positions[2][1] + 0.1)),
        (A_B,      ((positions[0][0] + positions[1][0]) / 2 - 0.00,
                    (positions[0][1] + positions[1][1]) / 2 + 0.02)),
        (A_C,      ((positions[0][0] + positions[2][0]) / 2 - 0.04,
                    (positions[0][1] + positions[2][1]) / 2 + 0.04)),
        (B_C,      ((positions[1][0] + positions[2][0]) / 2 + 0.03,
                    (positions[1][1] + positions[2][1]) / 2 + 0.04)),
        (A_B_C,    ((positions[0][0] + positions[1][0] + positions[2][0]) / 3,
                    (positions[0][1] + positions[1][1] + positions[2][1]) / 3))
    ]

    def draw_text(text, pos, bold_title=None):
        if not text:
            return
        lines = sorted(text)
        if bold_title:
            # Apply bold formatting only to the label line
            block = r"$\bf{" + bold_title + r"}$" + '\n\n' + '\n'.join(lines)
        else:
            block = '\n'.join(lines)
        ax.text(pos[0], pos[1], block, fontsize=10, ha='center', va='center')

    # Add set names to only regions
    draw_text(only_A, region_texts[0][1], labels[0] if bold_labels else None)
    draw_text(only_B, region_texts[1][1], labels[1] if bold_labels else None)
    draw_text(only_C, region_texts[2][1], labels[2] if bold_labels else None)

    # Add intersection content (no titles)
    for region, pos in region_texts[3:]:
        draw_text(region, pos)

    ax.set_xlim(0.2, 1.15)
    ax.set_ylim(0.2, 1.15)
    ax.set_aspect('equal')
    ax.axis('off')

    plt.title("Venn Diagram", fontsize=14)

    if save_path:
        plt.savefig(save_path, dpi=dpi, bbox_inches='tight')

    plt.show()
