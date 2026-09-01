# Image Style Clone Skill｜图片风格蒸馏与复刻

> 给 AI 一组同风格图片，不再靠“像不像”的玄学描述：先去 UI / 水印 / 杂项，再逐图 JSON 化，提取跨图共识 Style DNA，最后把任意新场景编译成同风格 Prompt 并出图。

## 一句话工作流

```text
参考图
  ↓
标准化：去 UI / 字幕 / 水印 / 截图边框 / 干扰项
  ↓
逐图视觉 JSON
  ↓
跨图共识：Invariant / Variable / Outlier
  ↓
Style DNA
  ↓
用户新关键词 / 场景 / 想法
  ↓
Prompt Compiler
  ↓
同风格最终提示词 + 生成图片
```

## 为什么不是“直接让 AI 模仿这几张图”？

因为直接模仿很容易把错误的东西学进去：

- 截图里的点赞按钮，被当成视觉风格；
- 字幕 / 水印，被写进 prompt；
- 某一张图里的具体人物，被误认为整个系列都必须出现；
- 一张离群图，把其他 7 张稳定风格带偏；
- 最后只剩“电影感、唯美、高级、治愈”这种无法复现的形容词。

这个 Skill 把问题拆成 **证据提取 → 共识聚合 → Prompt 编译** 三层。

## 核心设计

### 1. Normalize first

默认把以下内容从风格分析中移除：

`UI / status bar / buttons / captions / watermark / logo / device frame / cursor / editor guides`

遮挡区域如果无法恢复，就标记为 `unknown`，不会凭空脑补。

### 2. Per-image JSON

每张图独立提取：

- medium / rendering
- shape language
- edge / line
- composition
- camera / perspective
- lighting
- palette relationships
- material / texture
- depth / focus
- detail density
- atmosphere
- motion language
- recurring motifs
- negative evidence

**内容与风格分开记录。**

### 3. Cross-image consensus

候选特征被分成：

- `INVARIANT`：系列核心风格不变量
- `VARIABLE`：同风格内可变化部分
- `OUTLIER`：离群/偶发特征
- `UNKNOWN`：证据不足

默认不会让一张最花哨的图支配整个风格。

### 4. Style DNA + Prompt Compiler

先得到与具体题材无关的 `style_prompt_base`，再把用户新输入的人物、场景、动作、时间、天气、构图要求和画幅注入进去。

用户只修改一个维度时，Skill 只覆盖那个维度，不会把整个视觉系统一起改掉。

## 目录

```text
image-style-clone/
├── SKILL.md
├── README.md
├── schemas/
│   └── style-dna.schema.json
├── references/
│   ├── normalization.md
│   ├── style-dimensions.md
│   ├── aggregation.md
│   └── prompt-compiler.md
├── examples/
│   └── style_profile.example.json
└── evals/
    └── cases.yaml
```

## 使用方式

把整个目录放进支持 Agent Skills 的环境，或直接把 `SKILL.md` 提供给具备图像理解 + 图像生成能力的 Agent。

然后给它一组参考图，例如：

```text
分析这 7 张图的共同视觉风格。
先去掉截图里的 UI、字幕、水印和边框；
逐张总结成 JSON，再提取总 Style DNA。
接下来把场景改成“巨大橘猫躺在悉尼地铁车厢里，肚皮朝天睡觉”，
保留其他视觉风格不变。
最后给我最终 prompt，并直接出图。
```

## JSON contract

见 [`schemas/style-dna.schema.json`](schemas/style-dna.schema.json)。

完整示例：[`examples/style_profile.example.json`](examples/style_profile.example.json)。

## 设计原则

- 多图共识 > 单图强特征
- 具体主体 ≠ 风格
- UI 默认是污染
- 被遮挡区域 ≠ 证据
- 多风格混入时先聚类，不强行平均
- 用户明确 override > 参考图内容
- Prompt 使用可观察视觉特征，不靠形容词堆砌

## Limitations

- 参考图越少，Style DNA 置信度越低。
- 如果 UI / 水印遮挡面积过大，无法可靠恢复被遮挡的风格证据。
- 不同图像生成模型对同一 Prompt 的响应不同；Style DNA 负责提高可迁移性，但不能保证像素级一致。
- 本项目强调“视觉语言复用”，不是逐像素复制原图。

## License

MIT
