from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal


BBox = tuple[int, int, int, int]


@dataclass(frozen=True)
class TargetSize:
    width: int
    height: int

    @classmethod
    def parse(cls, value: str) -> "TargetSize":
        raw = value.lower().replace("*", "x")
        width, height = raw.split("x", 1)
        return cls(width=int(width), height=int(height))


@dataclass
class ProductLayer:
    image_path: Path
    mask_path: Path
    bbox: BBox
    locked: bool = True


@dataclass
class AdaptationManifest:
    mode: Literal["source_decompose", "product_upload"]
    target: TargetSize
    product: ProductLayer
    source_image: Path | None = None
    reference_image: Path | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
