from __future__ import annotations

import argparse
from pathlib import Path

from .manifest import TargetSize
from .pipeline import run_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Run ecommerce image adaptation MVP.")
    parser.add_argument("--product", type=Path, help="Standalone product image path.")
    parser.add_argument("--source", type=Path, help="Source creative image path.")
    parser.add_argument("--reference", type=Path, help="Optional reference image path.")
    parser.add_argument("--target", required=True, help="Target size, for example 1080x1920.")
    parser.add_argument("--out", type=Path, required=True, help="Output image path.")
    parser.add_argument("--work-dir", type=Path, default=Path("data/manifests/current"))
    parser.add_argument("--api-config", type=Path, default=Path("api.local.json"))
    args = parser.parse_args()

    report = run_pipeline(
        target=TargetSize.parse(args.target),
        out_path=args.out,
        work_dir=args.work_dir,
        product_image=args.product,
        source_image=args.source,
        reference_image=args.reference,
        api_config=args.api_config,
    )

    print("passed:", report.passed)
    print("checks:", report.checks)
    print("metrics:", report.metrics)
    if report.issues:
        print("issues:", report.issues)


if __name__ == "__main__":
    main()
