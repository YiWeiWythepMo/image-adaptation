# Image Adaptation

A compact AI skill for adapting ecommerce images to new aspect ratios and placements while preserving the product, required overlays, and the visual meaning of the original scene.

The skill treats adaptation as a layout problem rather than a simple resize. It decides what should remain dominant, what can be cropped, what needs to be extended or repaired, and when a cleaner background reconstruction will produce a stronger commercial image.

## What it does

- Preserves the identity and core appearance of locked products or subjects
- Protects required logos, labels, text, badges, and other overlays
- Maintains important background elements and scene semantics
- Chooses a composition suited to the target ratio or placement
- Allows controlled repair or reconstruction when literal outpainting would look weak
- Validates the final image against a consistent checklist

## When to use it

Use this skill when an existing ecommerce image must be adapted for another placement while remaining recognizably based on the source, for example:

- square product image to a wide marketplace banner
- desktop hero image to a vertical mobile placement
- campaign creative to a new advertising ratio
- product image that needs additional copy space
- composition repair after cropping or canvas extension

It is not intended for redesigning, replacing, reshaping, or materially altering the product.

## Workflow

The skill uses a three-part workflow:

1. **Plan** — identify locked subjects, protected background elements, overlays that must survive, and the best layout strategy.
2. **Edit** — turn that plan into a short, strict image-editing instruction for the target ratio or placement.
3. **Validate** — check subject fidelity, background semantics, overlays, ratio, and overall layout quality.

## Output contract

### Stage 1: planning

```json
{
  "locked_subjects": [],
  "protected_background": [],
  "preserved_overlays": [],
  "layout_advice": ""
}
```

### Stage 2: editing instruction

A concise prompt that states:

- the target ratio or usage
- the subjects that must remain unchanged
- overlays and background elements that must be preserved
- the intended crop, extension, repositioning, repair, or reconstruction
- an explicit prohibition on product redesign

### Validation

```json
{
  "subjects_preserved": true,
  "background_semantics_preserved": true,
  "overlays_preserved": true,
  "target_ratio_correct": true,
  "layout_quality": "acceptable",
  "issues": []
}
```

`layout_quality` is either `acceptable` or `needs_revision`. Any problems are listed as concrete issues, such as subject distortion, missing text, altered logos, lost scene semantics, weak composition, or an incorrect ratio.

## Example request

> Adapt this product image to a 16:9 marketplace hero. Keep the microwave and its control panel unchanged, preserve all readable product text, extend the kitchen environment naturally, and leave useful negative space for campaign copy.

If image generation is available, the skill returns the generated result followed by validation JSON. If only planning is available, it returns the Stage 1 JSON and the Stage 2 editing prompt.

## Sample image

![Sample ecommerce image](sample_images/4-1-Time%20and%20Weight%20Defrost.jpg)

## Installation

Place this repository in the skills directory used by your AI agent, keeping `SKILL.md` at the repository root, or add the repository through your agent's skill installation workflow.

```bash
git clone https://github.com/YiWeiWythepMo/image-adaptation.git
```

Then invoke the skill with an input image, a target ratio or placement, and any subjects, overlays, or background details that must be preserved.

## Repository structure

```text
image-adaptation/
├── SKILL.md
├── README.md
└── sample_images/
```

The detailed behavior, hard constraints, prompt format, and validation rules are defined in [SKILL.md](SKILL.md).

## Changelog

### 2026-09-17 — Initial documentation

- Added the project overview and supported ecommerce adaptation scenarios.
- Documented the planning, editing, and validation workflow.
- Added output contracts, an example request, installation guidance, and a sample image preview.
