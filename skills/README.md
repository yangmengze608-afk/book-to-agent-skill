# Skills

这个目录是 **Ykmmz Agent Skills** 的多 Skill 索引层。

目标不是把所有东西都堆在仓库根目录，而是逐步收敛成统一结构：

```text
skills/
├── book-to-agent/
└── image-style-clone/
```

## 当前状态

| Skill | Path | 状态 | 说明 |
|---|---|---:|---|
| Book → Agent Skill | `skills/book-to-agent/` | ✅ 已接入 | 文档入口已迁入；为兼容现有 CLI / taxonomy / prompts / schemas，部分实现仍保留在仓库根目录。 |
| Image Style Clone | `skills/image-style-clone/` | ✅ 已接入 | 完整 Skill、references、schema、example、evals 已并入。 |

## 迁移原则

1. **先建立统一入口，再逐步迁移底层实现**，避免为了“结构漂亮”打断现有功能。
2. **根目录继续兼容** 已存在的 `book-to-agent-skill` 路径与工作流。
3. **每个 Skill 都尽量自带**：
   - `SKILL.md`
   - `README.md`
   - `references/`
   - `schemas/`
   - `examples/`
   - `evals/`
4. **Progressive disclosure**：根 Skill 保持精炼，细节下沉到 `references/`。

## 下一步

- 继续把 Book → Agent Skill 的 supporting assets（如部分 prompts / taxonomy / schemas）逐步内聚到 `skills/book-to-agent/`；
- 为各个 Skill 增加独立英文 README；
- 增加统一安装 / 索引 / routing 规范。
