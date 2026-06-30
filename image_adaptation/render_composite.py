from __future__ import annotations

from pathlib import Path

from PIL import Image

from .layout_planner import LayoutPlan
from .manifest import AdaptationManifest


def render_composite(
    *,
    manifest: AdaptationManifest,
    layout: LayoutPlan,
    background_path: Path,
    out_path: Path,
) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    canvas = Image.open(background_path).convert("RGBA").resize(
        (layout.canvas_width, layout.canvas_height)
    )
    product = Image.open(manifest.product.image_path).convert("RGBA")
    product = product.resize((layout.product.width, layout.product.height), Image.LANCZOS)
    canvas.alpha_composite(product, (layout.product.x, layout.product.y))
    canvas.convert("RGB").save(out_path)
    return out_path
