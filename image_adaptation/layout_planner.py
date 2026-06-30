from __future__ import annotations

from dataclasses import dataclass

from PIL import Image

from .manifest import AdaptationManifest
from .providers.llm_adapter import LLMAdapter


@dataclass(frozen=True)
class LayerPlacement:
    layer_id: str
    x: int
    y: int
    width: int
    height: int
    z: int = 10
    locked_identity: bool = True


@dataclass(frozen=True)
class LayoutPlan:
    canvas_width: int
    canvas_height: int
    product: LayerPlacement
    background_mode: str = "extend_or_reconstruct_background_only"


def plan_layout(manifest: AdaptationManifest, llm: LLMAdapter | None = None) -> LayoutPlan:
    if llm and llm.is_configured:
        plan = llm.plan_layout(manifest)
        if plan:
            return plan

    return _fallback_centered_layout(manifest)


def _fallback_centered_layout(manifest: AdaptationManifest) -> LayoutPlan:
    canvas_w = manifest.target.width
    canvas_h = manifest.target.height
    image = Image.open(manifest.product.image_path).convert("RGBA")
    product_w, product_h = image.size

    max_w = int(canvas_w * 0.78)
    max_h = int(canvas_h * 0.68)
    scale = min(max_w / product_w, max_h / product_h, 1.0)
    out_w = max(1, int(product_w * scale))
    out_h = max(1, int(product_h * scale))
    x = (canvas_w - out_w) // 2
    y = int((canvas_h - out_h) * 0.52)

    return LayoutPlan(
        canvas_width=canvas_w,
        canvas_height=canvas_h,
        product=LayerPlacement(
            layer_id="product",
            x=x,
            y=y,
            width=out_w,
            height=out_h,
        ),
    )
