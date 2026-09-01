<div align="center">

# Ykmmz Agent Skills

**把真正可复用的方法，做成 Agent 能稳定调用的能力。**

**简体中文** · [English](./README_EN.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent-Skills-black)](./skills/README.md)

</div>

---

## 这是什么？

**Ykmmz Agent Skills** 是一个持续扩展的开源 Agent Skill 仓库。

这里不想堆一堆零散 Prompt。目标是把一种真正可重复的方法，沉淀成 Agent 可以**触发、执行、校验、复用**的能力。

一个值得长期保留的 Skill，理想情况下应该包含：

- 清楚、可执行的 `SKILL.md`；
- 明确的 Use / Do Not Use 边界；
- 必要时配套 schema、脚本或确定性流程；
- progressive disclosure：主 Skill 保持精炼，深度内容下沉到 `references/`；
- 能测试触发、应用、忠实度与边界情况的 eval；
- 对不确定性诚实，而不是为了完整感去编造结论。

## 仓库结构

```text
.
├── README.md
├── README_EN.md
├── SKILL.md                     # 当前根入口：Book → Agent Skill（兼容保留）
├── skills/
│   ├── README.md                # 多 Skill 索引
│   ├── book-to-agent/
│   │   ├── README.md
│   │   └── SKILL.md
│   └── image-style-clone/
│       ├── README.md
│       ├── SKILL.md
│       ├── references/
│       ├── schemas/
│       ├── examples/
│       └── evals/
└── ...                          # 其余原有 Book → Agent supporting assets
```

你也可以直接查看 [`skills/README.md`](./skills/README.md) 作为总目录。

## Skills

| Skill | 路径 | 能做什么 | 状态 |
|---|---|---|---|
| **Book → Agent Skill** | [`skills/book-to-agent/`](./skills/book-to-agent/README.md) | 把一本书蒸馏成一个可复用 Agent Skill：先分类，再按类别选择蒸馏策略，同时保留来源与 eval。 | ✅ 可用 |
| **Image Style Clone** | [`skills/image-style-clone/`](./skills/image-style-clone/README.md) | 清洗参考图 → 逐图 JSON → 提取跨图 Style DNA → 注入新场景 → 编译同风格生图 Prompt。 | ✅ 可用 |

> 仓库最初是单一的 `book-to-agent-skill` 项目。现在正在升级成更通用的 Agent Skill 总库，因此采用“**入口先统一，底层渐进迁移**”策略：先把各个 Skill 放到 `skills/` 里形成稳定入口，再逐步把底层 supporting assets 内聚过去，避免破坏已有工作流。

---

# Book → Agent Skill

> **一本书 → 一个可复用 Skill。先分类，再蒸馏。**

输入一本书（`.pdf` / `.epub` / `.txt` / `.md`），先判断它真正提供的**能力类型**，再调用对应类别的蒸馏策略，最终生成一个 Agent Skill，而不是一本“高级摘要”。

```text
一本书
  ↓
能力分类
  ↓
类别专属蒸馏策略
  ↓
ONE reusable Agent Skill
  ├── SKILL.md
  ├── BOOK.yaml
  ├── references/
  └── evals/cases.yaml
```

真正的成功标准不是“它知不知道这本书讲了什么”，而是：

> **一个新的 Agent，能不能按照这本书的方法去处理一个新的问题。**

完整入口：[`skills/book-to-agent/README.md`](./skills/book-to-agent/README.md)

## 为什么一定要先分类？

因为决策类书、心理学书、工程书，本来就不应该使用同一个“总结核心观点”模板。

当前 taxonomy 包含 16 个能力类别：

`decision-making` · `investing-finance` · `business-strategy` · `psychology-behavior` · `research-science` · `learning-education` · `writing` · `communication-negotiation` · `productivity` · `leadership-management` · `technology-engineering` · `creativity-design` · `philosophy-thinking` · `health-performance` · `reference-knowledge` · `other`

每个类别都会调用 `taxonomy/distillation_profiles/` 下自己的蒸馏 profile，决定：

- 该重点提取什么；
- 哪些地方必须保持认识论上的谨慎；
- `SKILL.md` 必须有哪些部分；
- eval 应该重点测试什么。

## 四类内容标签

为了避免 Agent 把“自己的推断”伪装成“作者原话”，references 中的内容明确分成：

- `SOURCE FACT` —— 来源明确陈述的事实或方法；
- `AUTHOR CLAIM` —— 作者自己的主张、建议或判断；
- `EVIDENCE` —— 来源中引用或依赖的证据；
- `DISTILLER INFERENCE` —— 蒸馏过程中为了执行而得到的推论，必须说明它从哪里推出来。

## 安装

```bash
git clone https://github.com/yangmengze608-afk/book-to-agent-skill.git
cd book-to-agent-skill
python -m venv venv && source venv/bin/activate
pip install -e ".[dev]"
```

> 仓库刚完成 rename。GitHub 会对旧地址做重定向；等连接器刷新出新的 canonical repo 名后，这里的安装命令会切到最终地址。

## 使用

```bash
book2skill init ./book.epub --workspace ./ws
book2skill distill --workspace ./ws
book2skill finalize --workspace ./ws
```

快捷入口：

```bash
book2skill run ./book.epub --workspace ./ws
book2skill doctor
```

## Eval Contract

每个生成出来的 book skill 至少包含 18 个 eval：

- 5 个 positive trigger；
- 5 个 negative trigger；
- 5 个 application；
- 3 个 edge / fidelity case。

## 我希望这个仓库坚持的原则

1. **能力 > 摘要** —— Skill 应该让 Agent 会做事，而不是多背了一份笔记。
2. **证据 > 感觉** —— 关键结论尽量可追溯。
3. **诚实表达不确定性** —— 不为了“完整”假装确定。
4. **Progressive Disclosure** —— `SKILL.md` 保持可执行，深度内容下沉到 `references/`。
5. **默认带 Eval** —— Markdown 写得漂亮不等于 Skill 真能工作。
6. **一个 Skill 一个清楚的工作** —— 触发条件与边界必须容易理解。

## Roadmap

- [x] Book → Agent Skill
- [x] Image Style Clone
- [x] 统一 `skills/` 索引入口
- [ ] 继续把 Book → Agent Skill supporting assets 迁入 `skills/book-to-agent/`
- [ ] 每个 Skill 增加独立英文 README
- [ ] Skill 索引与统一安装规范
- [ ] Cross-skill routing
- [ ] 持续加入更多中文优先、真正可执行的 Agent Skills

## License

MIT，见 [LICENSE](./LICENSE)。

对于由书籍蒸馏出来的 Skill，不要把受版权保护的完整书籍文本提交到仓库中；蒸馏结果应当是转化性的、改写后的，并尽可能保留来源信息。
