# CREATE-ENOUGH-ITEMS CLIENT DOMAIN

## OVERVIEW
`client/` 是 CEI 的客户端启动域（1 个 Java 文件）：客户端代理在构造阶段提前加载 EMI 折叠组规则，早于任何 EMI 界面构建。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 客户端代理 | `client/ClientProxy.java` |
| 折叠组规则加载 | `utils/emi/collapsible/CEICollapsibleGroups.java`（由 ClientProxy 构造函数调用） |

## CONVENTIONS
- `ClientProxy` 继承 `CommonProxy`，并标注 `@Mod.EventBusSubscriber(modid = CreateEnoughItems.MODID, bus = Mod.EventBusSubscriber.Bus.MOD, value = Dist.CLIENT)`；客户端初始化在此，公共注册留在 `common/CommonProxy.java`。
- `ClientProxy` 构造函数先 `super()`（触发 `CommonProxy.init()`），再调用 `CEICollapsibleGroups.loadRules()`，保证首帧 EMI 界面交互前规则已就绪。
- 仅客户端类不得出现在公共路径下。

## ANTI-PATTERNS
- 让仅客户端类可从公共路径访问。
- 把折叠组规则加载挪回惰性路径（`rebuild()`），导致首次 EMI 交互时分组规则尚未就绪。

## SCOPE
适用于 `src/main/java/com/ctnh/cei/client`。

## READ WHEN
- 改动 CEI 客户端启动流程或折叠组规则加载时机。

## SOURCE OF TRUTH
- `client/ClientProxy.java` 与 `CreateEnoughItems.java` 的代理接线。

## WORKFLOW
1. 在 `CreateEnoughItems.java` 核对代理接线（`DistExecutor.unsafeRunForDist`）。
2. 确认 `CEICollapsibleGroups.loadRules()` 在任何 EMI 界面访问之前被调用。
3. 跑 `:modules:Create-Enough-Items:build`。
