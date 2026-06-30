from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from PIL import Image

from .layout_planner import LayoutPlan
from .manifest import AdaptationManifest


@dataclass
class QualityReport:
    passed: bool
    checks: dict[str, bool] = field(default_factory=dict)
    metrics: dict[str, float] = field(default_factory=dict)
    issues: list[str] = field(default_factory=list)


def run_quality_checks(
    *,
    manifest: AdaptationManifest,
    layout: LayoutPlan,
    output_path: Path,
    min_product_ssim: float = 0.985,
) -> QualityReport:
    report = QualityReport(passed=True)
    output = Image.open(output_path).convert("RGB")

    size_ok = output.size == (manifest.target.width, manifest.target.height)
    _record(report, "target_size", size_ok, "Output size does not match target size.")

    bbox_ok = (
        layout.product.x >= 0
        and layout.product.y >= 0
        and layout.product.x + layout.product.width <= manifest.target.width
        and layout.product.y + layout.product.height <= manifest.target.height
    )
    _record(report, "product_inside_canvas", bbox_ok, "Product placement exceeds canvas.")

    similarity = _product_mask_similarity(manifest=manifest, layout=layout, output=output)
    report.metrics["product_mask_similarity"] = similarity
    _record(
        report,
        "product_identity",
        similarity >= min_product_ssim,
        "Product pixels differ from the locked product layer.",
    )

    report.passed = all(report.checks.values())
    return report


def _record(report: QualityReport, name: str, passed: bool, issue: str) -> None:
    report.checks[name] = passed
    if not passed:
        report.issues.append(issue)


def _product_mask_similarity(
    *,
    manifest: AdaptationManifest,
    layout: LayoutPlan,
    output: Image.Image,
) -> float:
    product_rgba = Image.open(manifest.product.image_path).convert("RGBA")
    product_rgba = product_rgba.resize((layout.product.width, layout.product.height), Image.LANCZOS)
    product = product_rgba.convert("RGB")
    mask = np.asarray(product_rgba.getchannel("A")) > 250
    region = output.crop(
        (
            layout.product.x,
            layout.product.y,
            layout.product.x + layout.product.width,
            layout.product.y + layout.product.height,
        )
    )
    product_arr = np.asarray(product).astype(np.float32)
    region_arr = np.asarray(region).astype(np.float32)
    if not mask.any():
        return 0.0
    diff = np.abs(product_arr[mask] - region_arr[mask])
    mean_diff = float(diff.mean()) if diff.size else 255.0
    return max(0.0, 1.0 - mean_diff / 255.0)
