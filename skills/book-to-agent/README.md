# Book → Agent Skill

> **一本书 → 一个可复用 Agent Skill。先分类，再蒸馏。**

这是 `Ykmmz Agent Skills` 仓库中的书籍蒸馏 Skill 入口。

## 它做什么？

输入一本书（`.pdf` / `.epub` / `.txt` / `.md`），先判断它真正提供的**能力类型**，再调用该类别专属的蒸馏策略，输出一个真正可被 Agent 调用的 Skill，而不是普通摘要。

## 当前迁移状态

为了不破坏已经存在的 CLI 和项目结构，当前采用**渐进式迁移**：

- 这个目录承担 **多 Skill 索引入口**；
- 仓库根目录仍保留当前 Book → Agent Skill 的实现与兼容路径；
- supporting assets（如 `taxonomy/`、`prompts/`、`schemas/`、部分示例和代码）会逐步迁入本目录。

所以如果你现在是第一次接触本项目：

- 看这里了解这个 Skill 在总库中的位置；
- 看仓库根目录的 `README.md` 获取完整项目介绍；
- 看仓库根目录的 `SKILL.md` 获取当前最完整的操作手册；
- 看 `../../taxonomy/`、`../../prompts/`、`../../schemas/` 获取 supporting assets。

## 结构目标

长期目标是收敛成：

```text
skills/book-to-agent/
├── SKILL.md
├── README.md
├── references/
├── taxonomy/
├── prompts/
├── schemas/
├── examples/
└── evals/
```

## 核心原则

- **能力 > 摘要**：目标是让 Agent 会按书的方法做事。
- **分类优先**：不同类别的书，不应用同一种蒸馏模板。
- **证据可追溯**：关键结论尽量保留来源。
- **诚实处理不确定性**：不用假确定掩盖模糊性。
- **默认带 eval**：Skill 的完成标准不是 Markdown 好看，而是能触发、能应用、不过度延伸。

## 兼容说明

如果你已经在使用根目录的 `book2skill` 工作流，当前无需改命令；本次变更先做信息架构升级，不主动打断旧用法。
