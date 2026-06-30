# Image Adaptation

MVP pipeline for ecommerce image adaptation with strict product preservation.

The core rule is simple: the product is never regenerated. Python extracts or accepts a locked product layer, the layout model only returns coordinates, the image generation model only extends or creates background, and final rendering pastes the original product pixels back onto the canvas.

## Capabilities

- Supports source-image decomposition and standalone product-image upload.
- Keeps product identity locked by treating the product as a protected layer.
- Uses an LLM adapter for layout plans without letting the LLM edit pixels.
- Uses a Nano Banana Pro adapter boundary for background expansion.
- Runs automatic quality gates before human review.
- Keeps local API credentials out of GitHub through `api.local.json`.

## MVP workflow

```text
input image or product image
  -> layer decomposition / product preprocessing
  -> structured manifest
  -> LLM layout plan
  -> background expansion adapter
  -> deterministic render
  -> automatic quality check
  -> human review
```

## Quick start

```bash
python -m venv .venv
pip install -r requirements.txt
python -m image_adaptation.cli --product sample_images/4-1-Time\ and\ Weight\ Defrost.jpg --target 1080x1920 --out data/outputs/demo.png
```

On Windows PowerShell:

```powershell
python -m venv .venv
pip install -r requirements.txt
python -m image_adaptation.cli --product "sample_images/4-1-Time and Weight Defrost.jpg" --target 1080x1920 --out "data/outputs/demo.png"
```

## Local API configuration

Create `api.local.json` in the project root. This file is ignored by Git.

```json
{
  "llm": {
    "provider": "openai_or_other_llm",
    "api_key": "fill-your-llm-api-key",
    "base_url": "optional-api-gateway",
    "model": "layout-model-name"
  },
  "image_generation": {
    "provider": "nano_banana_pro",
    "api_key": "fill-your-nano-banana-pro-api-key",
    "base_url": "provider-api-url",
    "model": "image-expansion-model-name"
  },
  "quality": {
    "min_product_ssim": 0.985,
    "max_color_delta": 3.0,
    "protect_padding_px": 16
  }
}
```

## Product preservation contract

- Product pixels in the final image must come from the uploaded product image or the extracted product layer.
- Image generation is only allowed on background, edge extension, and empty canvas regions.
- Protected masks must include padding around product edges.
- Quality checks fail the job if product identity, visible text, or logo regions appear altered.

## Repository layout

```text
image_adaptation/
  cli.py
  layer_decompose.py
  layout_planner.py
  manifest.py
  pipeline.py
  product_preprocess.py
  quality_check.py
  render_composite.py
  providers/
    llm_adapter.py
    nano_banana_adapter.py
docs/
  architecture.md
```
