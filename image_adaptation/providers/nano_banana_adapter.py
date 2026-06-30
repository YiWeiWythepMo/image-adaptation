from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageFilter

from image_adaptation.layout_planner import LayoutPlan
from image_adaptation.manifest import AdaptationManifest


class NanoBananaAdapter:
    def __init__(self, config_path: Path | None = None) -> None:
        self.config = _load_config(config_path).get("image_generation", {}) if config_path else {}
        self.is_configured = bool(self.config.get("api_key") and self.config.get("model"))

    def generate_background(
        self,
        *,
        manifest: AdaptationManifest,
        layout: LayoutPlan,
        out_path: Path,
    ) -> Path:
        """Generate or fallback-create a background with product protected."""
        out_path.parent.mkdir(parents=True, exist_ok=True)
        if self.is_configured:
            return self._call_provider(manifest=manifest, layout=layout, out_path=out_path)
        return self._fallback_background(manifest=manifest, layout=layout, out_path=out_path)

    def _call_provider(
        self,
        *,
        manifest: AdaptationManifest,
        layout: LayoutPlan,
        out_path: Path,
    ) -> Path:
        raise NotImplementedError(
            "Add the Nano Banana Pro HTTP call here. The request must send a protected product mask."
        )

    def _fallback_background(
        self,
        *,
        manifest: AdaptationManifest,
        layout: LayoutPlan,
        out_path: Path,
    ) -> Path:
        source = manifest.source_image or manifest.product.image_path
        image = Image.open(source).convert("RGB")
        image.thumbnail((layout.canvas_width, layout.canvas_height))
        canvas = Image.new("RGB", (layout.canvas_width, layout.canvas_height), (242, 242, 238))
        bg = image.resize((layout.canvas_width, layout.canvas_height)).filter(ImageFilter.GaussianBlur(28))
        canvas.paste(bg, (0, 0))
        canvas.save(out_path)
        return out_path


def _load_config(config_path: Path | None) -> dict[str, Any]:
    if not config_path or not config_path.exists():
        return {}
    return json.loads(config_path.read_text(encoding="utf-8"))
