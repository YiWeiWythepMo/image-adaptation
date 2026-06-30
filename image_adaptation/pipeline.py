from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

from .layer_decompose import build_manifest
from .layout_planner import plan_layout
from .manifest import TargetSize
from .providers.llm_adapter import LLMAdapter
from .providers.nano_banana_adapter import NanoBananaAdapter
from .quality_check import QualityReport, run_quality_checks
from .render_composite import render_composite


def run_pipeline(
    *,
    target: TargetSize,
    out_path: Path,
    work_dir: Path,
    product_image: Path | None = None,
    source_image: Path | None = None,
    reference_image: Path | None = None,
    api_config: Path | None = None,
) -> QualityReport:
    manifest = build_manifest(
        target=target,
        work_dir=work_dir,
        product_image=product_image,
        source_image=source_image,
        reference_image=reference_image,
    )
    layout = plan_layout(manifest, llm=LLMAdapter(api_config))
    background_path = work_dir / "background.png"
    NanoBananaAdapter(api_config).generate_background(
        manifest=manifest,
        layout=layout,
        out_path=background_path,
    )
    render_composite(
        manifest=manifest,
        layout=layout,
        background_path=background_path,
        out_path=out_path,
    )
    report = run_quality_checks(manifest=manifest, layout=layout, output_path=out_path)
    _write_manifest_debug(work_dir, manifest, layout, report)
    return report


def _write_manifest_debug(work_dir: Path, manifest: object, layout: object, report: QualityReport) -> None:
    import json

    work_dir.mkdir(parents=True, exist_ok=True)
    debug_path = work_dir / "manifest.debug.json"
    payload = {
        "manifest": asdict(manifest),
        "layout": asdict(layout),
        "quality": asdict(report),
    }
    debug_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
