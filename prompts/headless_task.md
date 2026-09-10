# CTNH-Docs 自动同步任务（CI / dsh headless）

你是本轮自动同步的**主代理**，工作目录是 CTNH-Docs 的检出根。目标：让 `ctnh-docs/references/` 下的模块指南与各模块源码当前状态一致。

## 输入

- `prompts/init_deep_update.md`：**必须完整遵守**的 init-deep 更新模式规范（含语言与风格、必须保留的声明、反模式）。
- `workspace/sync-plan.json`：本轮待处理模块、提交区间与 diff（已截断）。
- `workspace/modules-src/modules/<Module>/`：各模块源码（分支最新）。
- `ctnh-docs/references/<Module>/`：现有文档基线。

## 执行

1. 先读 `prompts/init_deep_update.md` 与 `workspace/sync-plan.json`，列出实际需要处理的模块（`modules` 字段）。
2. **每个模块启动一个后台 subagent 并行处理**：一次消息里同时发起全部委派，交给子代理的信息必须自包含——模块名、源码路径、文档路径、本轮提交摘要、必须遵守的规范路径与样例文档路径。子代理返回后按各自的汇报格式汇总。
3. 全部子代理结算后，主代理逐个复核：
   - 小节是否齐全、正文是否简体中文、路由链接是否指向真实存在的文件；
   - 反引号内的类名/路径能否在源码中找到（用 grep/read 抽查，重点看子代理声称"新增"或"删除"的项）；
   - 是否存在子代理互相矛盾或明显编造的内容。
   发现问题直接修补，不要把问题留给 CI。
4. 只需要改与源码变化相关的文档；无可核实变化的文档不要为了"改写而改写"。

## 硬性边界（违反会导致整轮作废）

- 只允许写 `ctnh-docs/references/<Module>/**/AGENTS.md`。
- **不要**改 `ctnh-docs/references/_architecture/AGENTS.md`（人工维护，CI 只读）。
- **不要**改 `scripts/`、`prompts/`、`.github/`、`README.md`、`README.zh_CN.md`、`workspace/`。
- **不要**执行 git add / commit / push；**不要**改 `scripts/state.json`（CI 在校验通过后单独推进水位）。
- 结论必须有源码证据；无法核实的断言宁可不写。

## 输出

最后用中文给出一段总结：处理了哪些模块、改了哪些文件、修正了哪些失效断言、哪些内容无法核实。
