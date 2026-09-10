# CTNH-ASTRAL UTILS DOMAIN

## OVERVIEW
Astral 的共享辅助工具（1 个 Java 文件）：`utils/ModUtils`，提供 Ad Astra 命名空间的 `ResourceLocation` 构造成快捷方法。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Ad Astra 资源路径构造 | `utils/ModUtils.AdAstraRL(String path)` |
| 唯一调用方 | `data/CATagPrefixes.java`（静态导入 `AdAstraRL`） |

## CONVENTIONS
- 辅助方法保持无注册依赖：`ModUtils` 只依赖 `earth.terrarium.adastra.AdAstra` 与 `ResourceLocation`，不引用本模块注册类。
- 需要构造其他 mod 命名空间路径时，先在这里补方法，不要在各域重复写 `ResourceLocation.tryBuild(MOD_ID, path)`。

## ANTI-PATTERNS
- 复制 CTNH-Lib `utils/` 已有的共享辅助逻辑。
- 在 `utils/` 里引入注册对象或世界生成依赖，制造初始化顺序问题。

## SCOPE
适用于 `src/main/java/com/ctnh/ctnhastral/utils`。

## READ WHEN
- 复用 Astral 全局辅助逻辑。
- 需要引用上游 mod 的资源路径。

## SOURCE OF TRUTH
- `utils/` 下的工具类。

## WORKFLOW
1. 先查 CTNH-Lib `utils/` 是否已有共享实现。
2. 改动后跑 `:modules:CTNH-Astral:build`。
