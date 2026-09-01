# Prompt Compiler

将结构化 Style DNA 编译为一条生成模型可执行的自然语言 prompt。

## 1. Input layers

### Layer A — User content
必须出现，优先级最高。

### Layer B — Core invariants
从 aggregate JSON 选 6–12 个最有区分度的风格锚点。

### Layer C — Variables
只加入与当前新场景兼容的可变项；不要全部塞进去。

### Layer D — Negative constraints
防止 UI、文字、风格漂移和常见模型偏差。

## 2. Recommended prompt skeleton

```text
[SUBJECT + ACTION] in/at [ENVIRONMENT], [STORY BEAT].
[COMPOSITION], [CAMERA / PERSPECTIVE].
Visual style: [MEDIUM], [SHAPE LANGUAGE], [EDGE / RENDERING], [CORE MATERIAL/TEXTURE].
Lighting: [LIGHTING SYSTEM]. Color: [PALETTE RELATIONSHIP].
Depth/detail: [DEPTH], [DETAIL DENSITY]. Atmosphere: [VISUALLY GROUNDED MOOD].
Avoid: [NEGATIVE CONSTRAINTS].
[ASPECT RATIO / OUTPUT CONSTRAINTS].
```

最终可以合并成自然流畅的一段，不必保留标签。

## 3. Style anchor selection

优先：

1. medium
2. shape language
3. composition
4. camera/perspective
5. lighting system
6. palette relationship
7. material/texture
8. edge behavior
9. depth/detail

如果某维度区分力很低，就省略。

## 4. User overrides

显式 override 按维度覆盖：

```text
reference DNA: low-key night lighting
user: “改成正午”
=> lighting = hard or diffuse daylight according to user intent
=> keep shape, camera, palette logic, material, composition rules unless incompatible
```

不要把 override 扩散到其他维度。

## 5. Negative prompt

默认考虑：

- UI, app chrome, interface buttons
- watermark, logo, username
- captions, subtitles, random typography
- borders/device mockups
- reference-specific objects not requested by the user

再加入 aggregate JSON 的 `negative_constraints`。

## 6. Prompt compression

如果 prompt 太长：

优先保留：content → composition → medium → shape → lighting → palette → texture → negatives。

删除：同义形容词、弱证据特征、与当前场景无关的 variables。

## 7. Never do this

- 不把 50 行 JSON 原样给生图模型。
- 不用“same style as references”代替具体视觉描述。
- 不只写“cinematic / cute / aesthetic / high quality”。
- 不把水印、签名、账号名当 Style Anchor。
