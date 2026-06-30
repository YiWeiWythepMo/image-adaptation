from __future__ import annotations

from pathlib import Path

from .manifest import AdaptationManifest, TargetSize
from .product_preprocess import preprocess_product


def build_manifest(
    *,
    target: TargetSize,
    work_dir: Path,
    product_image: Path | None = None,
    source_image: Path | None = None,
    reference_image: Path | None = None,
) -> AdaptationManifest:
    if product_image is None and source_image is None:
        raise ValueError("Either product_image or source_image is required.")

    product_source = product_image or source_image
    assert product_source is not None
    product = preprocess_product(product_source, work_dir / "layers")

    return AdaptationManifest(
        mode="product_upload" if product_image else "source_decompose",
        target=target,
        product=product,
        source_image=source_image,
        reference_image=reference_image,
        metadata={
            "product_identity_locked": True,
            "product_regeneration_allowed": False,
        },
    )
