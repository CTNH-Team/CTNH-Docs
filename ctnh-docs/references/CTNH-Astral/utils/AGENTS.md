# CTNH-ASTRAL UTILS DOMAIN

## OVERVIEW
Astral 的共享辅助工具（1 个 Java 文件）：`utils/ModUtils`，提供本模块命名空间 `ResourceLocation` 的短构造方法。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 本模块资源 id 构造 | `utils/ModUtils.ctnhAstralRL(String path)`（等价于 `CTNHAstral.id(path)`） |
| 领域 id 构造的权威入口 | `CTNHAstral.id(String name)`（`ResourceLocation.tryParse(MODID + ":" + name)`） |

## CONVENTIONS
- `ModUtils` 只依赖 `CTNHAstral.id(...)` 与 `ResourceLocation`，不引用任何注册类或世界生成类，避免初始化顺序问题。
- 模块内新增代码直接写 `CTNHAstral.id(path)`；`ModUtils.ctnhAstralRL(...)` 与它同义，不产生行为差异。
- 需要构造其他 mod 命名空间路径时，先在这里补方法，不要在各域重复写 `ResourceLocation.tryBuild(...)`。

## ANTI-PATTERNS
- 复制 CTNH-Lib `utils/` 已有的共享辅助逻辑。
- 在 `utils/` 里引入注册对象或世界生成依赖，制造初始化顺序问题。
- 让 `ModUtils` 与 `CTNHAstral.id(...)` 的解析规则分叉（例如一处用 `tryBuild`、一处用 `tryParse`）。

## SCOPE
适用于 `src/main/java/com/ctnh/ctnhastral/utils`。

## READ WHEN
- 复用 Astral 全局辅助逻辑。
- 新增跨域共享的 id / 路径构造方法。

## SOURCE OF TRUTH
- `utils/` 下的工具类与 `CTNHAstral.id(...)`。

## WORKFLOW
1. 先查 CTNH-Lib `utils/` 是否已有共享实现。
2. 改动后跑 `:modules:CTNH-Astral:build`。
