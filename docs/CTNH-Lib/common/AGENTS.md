# CTNH-LIB COMMON DOMAIN

## OVERVIEW
Shared server-side bootstrap: CommonProxy and the MultiblockHelper runtime item (2 Java files).

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Common proxy | `common/CommonProxy.java` |
| Runtime helper item | `common/MultiblockHelper.java` |

## CONVENTIONS
- `CommonProxy` initializes `CTNHLibNetworking`, registers the runtime helper item through GTCEu's registrate, and adds the `ctnhlib:filter_data` server data pack source. `GTProvidersRegistrar.init()` was removed in f9951f9; `CommonProxy.init()` is now a no-op (empty) and no longer touches Jade.
- `MultiblockHelper` is registered through GTCEu's registrate as a runtime helper item; it references `ForgeRegistries.BLOCKS` for its debug output string (not for recipe item resolution).

## ANTI-PATTERNS
- Do not add gameplay content to the common proxy; Lib hosts shared infrastructure only.
- Do not reintroduce Jade registrar calls in `CommonProxy`.

## SCOPE
Applies to `src/main/java/tech/vixhentx/mcmod/ctnhlib/common`.

## READ WHEN
- Changing Lib bootstrap, networking init, or the runtime helper item.

## SOURCE OF TRUTH
- `common/CommonProxy.java` and `CTNHLib.java`.

## WORKFLOW
1. Check `CommonProxy` initialization order before adding hooks.
2. Run `:modules:CTNH-Lib:build` after changes.
