# Architecture

## Goals

This project adapts ecommerce images into new ratios or placements while keeping the product completely consistent.

## Inputs

Two input modes are supported:

1. `source_image`: a full creative image that needs decomposition.
2. `product_image`: a standalone product image uploaded by the user.

The product upload path is preferred when exact product fidelity matters.

## Pipeline

1. Product preprocessing
   - Load product image.
   - Preserve alpha if present.
   - If the image has a flat background, estimate a mask.
   - Save product bbox, mask, and product metadata.

2. Layer decomposition
   - Build a manifest with background, product, overlays, masks, bbox, and target size.
   - Keep product as a locked layer.

3. Layout planning
   - LLM returns JSON layout instructions only.
   - The LLM may move, scale, and order layers.
   - The LLM may not modify product pixels.

4. Background generation
   - Nano Banana Pro adapter receives target canvas and protected masks.
   - Protected product regions are excluded from generation.
   - The fallback implementation creates a simple blurred background locally.

5. Deterministic rendering
   - Python composites the final image.
   - Product layer is pasted back after background generation.

6. Quality gates
   - Target size check.
   - Product bbox check.
   - Product similarity check.
   - Mask coverage check.
   - Optional OCR/logo checks can be added as stricter gates.

7. Human review
   - Reviewers compare source/product and output.
   - Review decisions are stored for future prompt and rule tuning.

## Non-negotiable rule

The final product must be visually identical to the uploaded or extracted product layer, except for deterministic resizing and placement.
