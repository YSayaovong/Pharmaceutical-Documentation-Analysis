"""
generate_visuals.py
Regenerates the diagrams in /visuals for the pharma-doc-analysis repo.

Run:
  python -m pip install numpy matplotlib
  python scripts/generate_visuals.py
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

def ensure_dirs(project_root: Path) -> Path:
    visuals = project_root / "visuals"
    visuals.mkdir(exist_ok=True)
    return visuals

def pharma_workflow(visuals: Path) -> None:
    out = visuals / "pharma_workflow.png"
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.axis("off")
    steps = ["Vendor", "Document\nSubmission", "QA/QC\nReview", "Compliance\nValidation", "Approval &\nRelease"]
    xs = np.linspace(0.6, 10.6, len(steps))
    for i, (x, label) in enumerate(zip(xs, steps)):
        p = FancyBboxPatch((x, 1.3), 1.7, 1.2, boxstyle="round,pad=0.2,rounding_size=0.12",
                           linewidth=1.2, edgecolor="black", facecolor="#e9f5ff")
        ax.add_patch(p)
        ax.text(x+0.85, 1.9, label, ha="center", va="center", fontsize=11, fontweight="bold")
        if i < len(steps)-1:
            ax.add_patch(FancyArrowPatch((x+1.9, 1.9), (xs[i+1]-0.1, 1.9),
                                         arrowstyle="-|>", mutation_scale=18, linewidth=1.2))
    ax.text(6, 3.2, "Pharmaceutical Vendor Documentation Workflow", ha="center", fontsize=14, fontweight="bold")
    plt.savefig(out, dpi=180, bbox_inches="tight")
    plt.close()

def compliance_risk_map(visuals: Path) -> None:
    out = visuals / "compliance_risk_map.png"
    risk = np.array([
        [1, 2, 3, 4],
        [2, 3, 4, 5],
        [1, 3, 4, 5],
        [1, 2, 3, 4],
    ])
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(risk, cmap="Reds")
    ax.set_title("Compliance Risk Heatmap", fontsize=13, fontweight="bold")
    ax.set_xticks([0,1,2,3]); ax.set_yticks([0,1,2,3])
    ax.set_xticklabels(["Low Impact", "Med", "High", "Critical"], rotation=15)
    ax.set_yticklabels(["Low Likelihood", "Med", "High", "Critical"])
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    plt.tight_layout()
    plt.savefig(out, dpi=180, bbox_inches="tight")
    plt.close()

def document_flowchart(visuals: Path) -> None:
    out = visuals / "document_flowchart.png"
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis("off")
    boxes = [
        ("Receive vendor document\n(PDF / scan / email)", (1, 4.5)),
        ("Classify document type\n(CoA / SDS / Calibration / Change)", (1, 3.4)),
        ("Extract key fields\n(lot, dates, specs, signatures)", (1, 2.3)),
        ("Validate completeness\n(required fields, formats)", (1, 1.2)),
        ("Route exceptions\n(missing/invalid → QA queue)", (1, 0.1)),
    ]
    for label, (x,y) in boxes:
        ax.add_patch(FancyBboxPatch((x,y), 8, 0.85, boxstyle="round,pad=0.2,rounding_size=0.12",
                                   linewidth=1.2, edgecolor="black", facecolor="#fff7e6"))
        ax.text(x+4, y+0.43, label, ha="center", va="center", fontsize=11, fontweight="bold")
    for i in range(len(boxes)-1):
        ax.add_patch(FancyArrowPatch((5, boxes[i][1][1]-0.05), (5, boxes[i+1][1][1]+0.95),
                                     arrowstyle="-|>", mutation_scale=18, linewidth=1.2))
    ax.text(5, 5.55, "Document Handling Flow (AI-Ready)", ha="center", fontsize=14, fontweight="bold")
    plt.savefig(out, dpi=180, bbox_inches="tight")
    plt.close()

def main():
    project_root = Path(__file__).resolve().parents[1]
    visuals = ensure_dirs(project_root)
    pharma_workflow(visuals)
    compliance_risk_map(visuals)
    document_flowchart(visuals)
    print("✅ Visuals regenerated in:", visuals)

if __name__ == "__main__":
    main()
