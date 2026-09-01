---
name: book-to-agent-skill
description: Turn a book (PDF/EPUB/TXT/MD) into one reusable Agent Skill - classify the book first, distill with a category-specific strategy second, with source provenance, four content-type tags, and an auto-generated eval suite. Use when the user asks to convert a book into an agent skill / claude skill / codex skill, distill a book's methods into a skill, or create a skill from a book.
---

# Book → Agent Skill

这是 `Ykmmz Agent Skills` 多 Skill 结构中的 **Book → Agent Skill** 入口文件。

## Current migration mode

当前仓库正在从单一项目升级为多 Skill 总库，因此本目录采用**兼容优先**策略：

- 本文件提供多 Skill 结构下的入口与边界；
- 书籍蒸馏的完整工作流、详细规则和 supporting assets 当前仍以仓库根目录为主；
- 你在执行此 Skill 时，应同时参考：
  - `../../SKILL.md`
  - `../../README.md`
  - `../../taxonomy/`
  - `../../prompts/`
  - `../../schemas/`

## Purpose

把一本书转化成一个**可复用的 Agent Skill**，让 Agent 能按照书的方法处理新问题，而不仅仅是知道书里讲了什么。

## Use When

- 用户要求“把这本书做成一个 skill”；
- 用户希望把书里的方法论沉淀成可触发的 Agent 能力；
- 用户要的是可执行能力，而不是普通摘要或 RAG 问答。

## Do Not Use When

- 用户只是想要摘要、读书笔记或 chat-with-PDF；
- 输入不是单本书；
- 文件是扫描版 PDF 且没有可用文本层；
- 用户想把一本书拆成多个 skill（本项目默认 one book → one skill）。

## Operating rule

当前执行时，以根目录版本的 **Book → Agent Skill** 工作流为准：

1. `init`：抽取文本、识别结构、建立工作区；
2. `classification`：判断主能力类别；
3. `distill`：按类别专属策略生成 `SKILL.md` 与 `references/`；
4. `eval`：生成触发、反触发、应用和 edge cases；
5. `finalize`：schema / 结构 / 来源校验并输出最终 skill。

## Hard principles

- 能力 > 摘要
- 分类优先
- 关键结论可追溯
- 诚实表达不确定性
- 默认携带 eval
- 一个 skill 做一个清楚的工作

## Migration note

这个文件的存在，是为了让仓库现在就具备统一的 `skills/<skill-name>/` 入口，而不需要一次性搬动全部底层实现。后续 supporting assets 会继续逐步迁入本目录。
