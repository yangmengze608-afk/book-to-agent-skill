# Cross-image Style Aggregation

## Goal

Aggregate repeated visual evidence into a reusable, content-independent Style DNA. Do not concatenate per-image descriptions.

## Feature classes

- `INVARIANT`: core style identity. Default heuristic: supported by >=70% of usable references, or slightly less with unusually strong and high-confidence visual evidence.
- `VARIABLE`: compatible variation inside the same style. Default support: 30–69%.
- `OUTLIER`: <=29% support and inconsistent with the dominant visual system, or sourced mainly from a clear outlier image.
- `UNKNOWN`: insufficient visible evidence.

These are heuristics, not statistical laws. With only 1–2 images, lower confidence rather than pretending the thresholds are meaningful.

## Weighting

Use this qualitative priority:

`visibility × cross-image support × confidence × distinctiveness`

A single visually loud image must not dominate several quieter but consistent references.

## Content leakage test

Before promoting any feature to Style DNA, ask:

> If the user replaced the subject, location, props, and story, would this feature still make sense as a visual rule?

If no, keep it in content, not style.

## Cluster before aggregate

If the set contains incompatible media or visual systems:

1. cluster by medium/rendering first;
2. compare composition/light/palette/shape within clusters;
3. select the largest and most internally coherent cluster as primary by default;
4. keep other clusters as alternatives;
5. never average photography + 3D + ink wash into one generic style.

## Confidence

Overall confidence should fall when:

- reference count is small;
- UI/overlay occlusion is large;
- references disagree strongly;
- key dimensions are invisible;
- the set contains several near-equal clusters.

## Variation budget

Record what can change without breaking identity:

- subject identity: usually free
- environment: usually free
- pose/action: usually free
- accent hue: often moderate
- camera angle: style-dependent
- shape language: often low variation
- rendering/material response: often low variation
- lighting system: style-dependent

The variation budget helps the prompt compiler adapt to new scenes without erasing the Style DNA.
