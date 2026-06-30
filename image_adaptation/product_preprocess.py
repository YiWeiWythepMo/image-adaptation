from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

from .manifest import BBox, ProductLayer


def preprocess_product(product_path: Path, work_dir: Path) -> ProductLayer:
    work_dir.mkdir(parents=True, exist_ok=True)
    image = Image.open(product_path).convert("RGBA")
    rgba = np.array(image)
    alpha = rgba[:, :, 3]

    if alpha.max() == 255 and alpha.min() == 255:
        alpha = _estimate_foreground_alpha(rgba[:, :, :3])

    bbox = _bbox_from_alpha(alpha)
    mask_path = work_dir / "product_mask.png"
    locked_product_path = work_dir / "product_locked.png"

    locked = rgba.copy()
    locked[:, :, 3] = alpha
    Image.fromarray(locked, "RGBA").save(locked_product_path)
    Image.fromarray(alpha, "L").save(mask_path)

    return ProductLayer(
        image_path=locked_product_path,
        mask_path=mask_path,
        bbox=bbox,
        locked=True,
    )


def _estimate_foreground_alpha(rgb: np.ndarray) -> np.ndarray:
    corners = np.array(
        [
            rgb[0, 0],
            rgb[0, -1],
            rgb[-1, 0],
            rgb[-1, -1],
        ],
        dtype=np.float32,
    )
    background = np.median(corners, axis=0)
    distance = np.linalg.norm(rgb.astype(np.float32) - background, axis=2)
    mask = (distance > 18).astype(np.uint8) * 255
    mask_image = Image.fromarray(mask, "L").filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(5))
    return np.asarray(mask_image)


def _bbox_from_alpha(alpha: np.ndarray) -> BBox:
    ys, xs = np.where(alpha > 0)
    if len(xs) == 0 or len(ys) == 0:
        height, width = alpha.shape[:2]
        return (0, 0, width, height)
    return (int(xs.min()), int(ys.min()), int(xs.max() + 1), int(ys.max() + 1))
