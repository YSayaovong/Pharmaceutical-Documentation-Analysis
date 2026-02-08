"""
scripts/generate_visuals.py

Generates professional, high-contrast visuals for the pharma-doc-analysis project.

Outputs (in ../visuals):
- pharma_workflow.png
- document_flowchart.png
- compliance_risk_map.png

Run (from project root):
  python -m pip install numpy matplotlib
  python scripts/generate_visuals.py
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# ---------------- Theme ----------------
NAVY = "#0B1F3B"
BG = "#F6F8FB"
BOX = "#FFFFFF"


# ---------------- Helpers ----------------
def _canvas(figsize):
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.axis("off")
    return fig, ax


def _save(fig, out: Path):
    out.parent.mkdir(exist_ok=True)
    fig.savefig(out, dpi=320, bbox_inches="tight", facecolor=BG)
    plt.close(fig)


# --------------------------------------------------------------------
# 1) Pharmaceutical Vendor Documentation Workflow (HORIZONTAL)
#    - boxes spaced out
#    - arrows fit cleanly within the empty gaps (no overlap, no reversal)
# --------------------------------------------------------------------
def pharma_workflow(visuals: Path) -> None:
    out = visuals / "pharma_workflow.png"
    fig, ax = _canvas((18, 5))

    ax.text(
        0.5, 0.88,
        "Pharmaceutical Vendor Documentation Workflow",
        ha="center", va="center",
        transform=ax.transAxes,
        fontsize=28, fontweight="bold", color=NAVY
    )

    steps = [
        "Vendor",
        "Document\nSubmission",
        "QA/QC\nReview",
        "Compliance\nValidation",
        "Approval\n& Release"
    ]

    n = len(steps)
    y = 0.42
    w = 0.13
    h = 0.24

    # Auto-fit layout so everything stays on the canvas
    left_margin = 0.06
    right_margin = 0.06
    available = 1.0 - left_margin - right_margin - (n * w)

    # If space is tight, shrink width slightly
    if available < 0.12:
        w = 0.115
        available = 1.0 - left_margin - right_margin - (n * w)

    # base gap between boxes (visible)
    gap = max(0.055, available / (n - 1))
    xs = [left_margin + i * (w + gap) for i in range(n)]

    # Draw boxes
    for x, label in zip(xs, steps):
        ax.add_patch(FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.02,rounding_size=0.04",
            linewidth=3, edgecolor=NAVY, facecolor=BOX,
            transform=ax.transAxes
        ))

        ax.text(
            x + w / 2, y + h / 2, label,
            ha="center", va="center",
            transform=ax.transAxes,
            fontsize=18, fontweight="bold", color=NAVY
        )

    # Draw arrows: compute the REAL gap between boxes and clamp margins
    for i in range(n - 1):
        gap_space = xs[i + 1] - (xs[i] + w)  # empty space between the boxes

        # margin must be less than half the gap, otherwise arrows reverse or overlap
        margin = min(gap_space * 0.22, (gap_space - 0.02) / 2)
        margin = max(margin, 0.01)  # small buffer so arrow never touches boxes

        start_x = xs[i] + w + margin
        end_x = xs[i + 1] - margin

        ax.add_patch(FancyArrowPatch(
            (start_x, y + h / 2),
            (end_x, y + h / 2),
            arrowstyle="-|>",
            mutation_scale=34,
            linewidth=3,
            color=NAVY,
            transform=ax.transAxes
        ))

    _save(fig, out)


# --------------------------------------------------------------------
# 2) Document Handling Flow (VERTICAL)
#    - title outside the boxes
#    - arrows fully between boxes
# --------------------------------------------------------------------
def document_flowchart(visuals: Path) -> None:
    out = visuals / "document_flowchart.png"
    fig, ax = _canvas((14, 13))

    ax.text(
        0.5, 0.94,
        "Document Handling Flow",
        ha="center", va="center",
        transform=ax.transAxes,
        fontsize=28, fontweight="bold", color=NAVY
    )

    steps = [
        "Receive vendor document (PDF / scan / email)",
        "Classify document type (CoA / SDS / Calibration / Change)",
        "Extract key fields (lot, dates, specs, signatures)",
        "Validate completeness (required fields, formats)",
        "Route exceptions (missing / invalid → QA queue)"
    ]

    x = 0.10
    w = 0.80
    h = 0.075
    gap = 0.12
    y_start = 0.82

    ys = []
    for i, label in enumerate(steps):
        y = y_start - i * (h + gap)
        ys.append(y)

        ax.add_patch(FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.02,rounding_size=0.04",
            linewidth=3, edgecolor=NAVY, facecolor=BOX,
            transform=ax.transAxes
        ))

        ax.text(
            x + w / 2, y + h / 2, label,
            ha="center", va="center",
            transform=ax.transAxes,
            fontsize=16, fontweight="bold", color=NAVY
        )

    for i in range(len(ys) - 1):
        y_top_box_bottom = ys[i]
        y_next_box_top = ys[i + 1] + h

        margin = gap * 0.30
        start_y = y_top_box_bottom - margin
        end_y = y_next_box_top + margin

        ax.add_patch(FancyArrowPatch(
            (0.5, start_y),
            (0.5, end_y),
            arrowstyle="-|>",
            mutation_scale=40,
            linewidth=3,
            color=NAVY,
            transform=ax.transAxes
        ))

    _save(fig, out)


# --------------------------------------------------------------------
# 3) Compliance Risk Heatmap (simple + readable)
# --------------------------------------------------------------------
def compliance_risk_map(visuals: Path) -> None:
    out = visuals / "compliance_risk_map.png"

    risk = np.array([
        [1, 2, 3, 4],
        [2, 3, 4, 5],
        [1, 3, 4, 5],
        [1, 2, 3, 4],
    ])

    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    im = ax.imshow(risk, cmap="Reds")

    ax.set_title("Compliance Risk Heatmap", fontsize=22, fontweight="bold", color=NAVY, pad=16)

    ax.set_xticks([0, 1, 2, 3])
    ax.set_yticks([0, 1, 2, 3])
    ax.set_xticklabels(["Low Impact", "Med", "High", "Critical"], fontsize=13)
    ax.set_yticklabels(["Low Likelihood", "Med", "High", "Critical"], fontsize=13)

    for i in range(risk.shape[0]):
        for j in range(risk.shape[1]):
            ax.text(
                j, i, str(risk[i, j]),
                ha="center", va="center",
                fontsize=13, fontweight="bold", color=NAVY
            )

    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.savefig(out, dpi=320, bbox_inches="tight", facecolor=BG)
    plt.close(fig)


# --------------------------------------------------------------------
# MAIN
# --------------------------------------------------------------------
def main():
    project_root = Path(__file__).resolve().parents[1]
    visuals = project_root / "visuals"
    visuals.mkdir(exist_ok=True)

    print("Writing visuals to:", visuals.resolve())

    pharma_workflow(visuals)
    document_flowchart(visuals)
    compliance_risk_map(visuals)

    print("✅ Visuals updated:", visuals.resolve())


if __name__ == "__main__":
    main()
