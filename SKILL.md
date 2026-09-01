---
name: image-style-clone-skill
description: Distill a reusable visual Style DNA from multiple reference images, first removing UI/overlays/noise from analysis, then converting each clean reference into JSON evidence, aggregating cross-image invariants/variables/outliers, merging the user's new subject or scene, and outputting a same-style generation prompt plus a generated image when an image tool is available. Use when a user asks to copy, match, reproduce, inherit, summarize, or continue the style of a set of images.
---

# Image Style Clone Skill

把一组参考图变成可复用的 **Style DNA**，再把用户的新关键词、场景或想法注入进去。

**Pipeline**

`References → Normalize → Per-image JSON → Consensus Style DNA → User Intent Merge → Prompt → Generate → QA`

最终默认只交付：

1. 同风格最终提示词；
2. 按提示词生成的图片（当前环境有图像生成工具时）。

中间 JSON 要完整生成，但除非用户要求，不必全部展示。

## Use When

- 用户给多张相近风格图片，要“照这个系列的感觉做新图”。
- 用户要先去掉截图 UI / 字幕 / 水印，再提取画风。
- 用户要把同一视觉风格迁移到新的主体、场景、动作或故事。

推荐 3–12 张参考图。1 张可分析，但只能得到低置信度单图描述；2 张只能初步判断共性。

## Do Not Use When

- 只是 OCR、翻译、识物或普通图片问答。
- 没有参考图，却要求声称“从图片提取了 Style DNA”。
- 用户要复制的是 UI/网页界面本身；此 Skill 默认把前端 UI 当干扰项。

# Operating Procedure

## Phase 1 — Audit the reference set

逐张判断：

- medium/rendering 是否一致；
- UI、文字、水印、边框、设备框、贴纸等污染；
- 遮挡比例；
- 是否可能是离群图；
- 有多少区域真正可用于判断风格。

如果明显包含多个风格，**先聚类，不要平均**。默认使用数量最多且内部一致性最高的主簇，其他记为 alternatives。详见 `references/aggregation.md`。

## Phase 2 — Normalize

保留原图，只处理分析副本或分析视野。

默认移除/忽略：

- status bar、导航、按钮、进度条、App/Web chrome；
- 后加字幕、标题、用户名、标签、评论气泡；
- 水印、平台 Logo、二维码；
- 设备 mockup、截图边框；
- 鼠标、选中框、编辑器参考线；
- 明显截图压缩/缩放伪影。

不要误删作品本身的文字、场景内招牌、原生漫画气泡、纸纹、笔触、颗粒等。

有图像编辑能力时可对分析副本 crop/mask/inpaint；没有时直接忽略污染区域。**被遮挡区域记为 unknown，禁止脑补成证据。**

完整规则见 `references/normalization.md`。

## Phase 3 — Per-image JSON

每张图先独立分析，不要先写总风格。

至少提取：

- medium / rendering
- subject treatment
- shape language / proportions
- line / edge behavior
- composition
- camera / perspective
- lighting
- palette relationships
- material / texture
- depth / focus
- motion language
- detail density
- atmosphere
- recurring motifs
- negative evidence
- contamination removed/ignored
- confidence by dimension

使用 `schemas/style-dna.schema.json`。

### Separate content from style

- “一只橘猫” = content
- “圆润体块、短肢、大头身比” = style
- “东京街头” = content
- “夜间低照度、湿地反射、局部霓虹高光、长焦压缩空间” = style

优先写可观察特征，不写空泛词。

差：`高级、唯美、治愈、电影感`。

好：`低饱和蓝灰基底 + 小面积暖黄点光；软阴影；主体边缘柔和逆光；背景对比度低于主体。`

维度词典见 `references/style-dimensions.md`。

## Phase 4 — Aggregate Style DNA

读取全部 per-image evidence，把每个候选特征归为：

- `INVARIANT`：核心不变量；
- `VARIABLE`：风格内部允许变化；
- `OUTLIER`：偶发/离群；
- `UNKNOWN`：证据不足。

默认启发式：≥70% 支持可进入 invariant，30–69% 更适合 variable，≤29% 通常是 outlier；参考图少时降低置信度，不机械套阈值。

权重优先：

`高可见度 × 多图支持 × 高置信度 > 单张强烈但孤立的特征`

生成 aggregate JSON，至少包含：

- `invariants`
- `variables`
- `outliers`
- `unknown`
- `negative_constraints`
- `variation_budget`
- `overall_confidence`
- `style_prompt_base`

`style_prompt_base` 必须与具体人物/地点/物件无关。示例见 `examples/style_profile.example.json`。

## Phase 5 — Parse the user's new idea

拆成：

**Required content**

- subject
- action/pose
- environment
- story beat
- props
- time/weather
- aspect ratio/framing
- required text if any

**Explicit style overrides**

用户明确说“保持画风但改成白天 / 更暖 / 改成长焦”时，只覆盖被点名维度；其余 Style DNA 保持。

用户明确的新内容优先于参考图内容。不要为了“像参考图”偷偷改回原来的主体或场景。

## Phase 6 — Compile final prompt

将 JSON 编译成自然语言 prompt，不要 JSON dump。

推荐顺序：

1. 主体 + 动作 + 场景
2. 构图 + 镜头 + 透视
3. 6–12 个最关键 Style Anchors
4. 光线 + 色彩关系
5. 材质 + 纹理 + 细节密度
6. 氛围 / 动态
7. negative constraints
8. 画幅 / 输出约束

不要依赖“same style as references”；要把风格写成可执行视觉特征。

完整编译规则见 `references/prompt-compiler.md`。

## Phase 7 — Deliver and generate

输出：

```text
Style DNA confidence: <0–1>

1. 同风格最终提示词
<final prompt>

2. 生成图片
<invoke image generation tool>
```

若有图像生成工具，直接生成，不再次确认。未指定比例时，用参考集主流比例；若参考集比例不一致，选择最适合用户新场景的比例。

若没有生图能力，明确只交付 prompt，不假装已经生成。

## Phase 8 — QA

生成后检查：

- **Content fidelity**：主体、场景、动作是否符合用户要求？
- **Style fidelity**：核心 invariants 是否保留？
- **Outlier control**：是否误吸收离群特征？
- **Contamination**：是否重新出现 UI、字幕、水印、Logo？
- **Drift**：是否只是题材像，却失去参考图结构性风格？

明显失败且工具允许时，最多主动修正一轮。

# Decision Rules

1. 多图共识优先于单图强特征。
2. 具体主体不是风格，除非其造型规律跨图稳定复现。
3. UI 默认是污染，除非用户明确要复制 UI 设计。
4. 被遮挡区域不是证据。
5. 多风格混入时先聚类。
6. 用户明确 override 高于参考图内容。
7. 用户只改一个维度，就只覆盖那个维度。
8. 风格相似度来自结构性特征组合，不来自形容词数量。

# Failure Modes

- **Screenshot contamination** → 回到 Normalize，去掉 UI/overlay。
- **Content leakage** → 把具体人物/物件移回 content，只保留跨图视觉规律。
- **Adjective soup** → 改写为镜头、光线、色彩、形状、材质、空间特征。
- **Incompatible averaging** → 聚类，选主簇。
- **One-image overfit** → 只保留跨图共识。
- **Hallucinated cleanup** → 遮挡区设为 unknown 并降低置信度。

# References

- `references/normalization.md` — 去 UI / 水印 / 杂项
- `references/style-dimensions.md` — 可观察风格维度
- `references/aggregation.md` — 跨图共识、聚类、置信度
- `references/prompt-compiler.md` — Style DNA → Prompt
- `schemas/style-dna.schema.json` — JSON contract
- `examples/style_profile.example.json` — 完整示例
- `evals/cases.yaml` — trigger / anti-trigger / fidelity / edge cases

# Final Quality Check

1. 原图未被覆盖。
2. UI / 水印 / 字幕没有进入 Style DNA。
3. 核心特征有多图证据或明确高置信理由。
4. 具体人物 / 地点 / 物件没有被错误固化为风格。
5. invariant / variable / outlier / unknown 已分开。
6. 用户新需求完整进入 final prompt。
7. prompt 可直接生图。
8. 有生图工具时已经实际调用；没有时明确说明限制。
