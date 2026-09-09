# CTPP CONFIG DOMAIN

## OVERVIEW
CTPP module configuration (2 Java files).

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Config entry | `config/MainConfig.java` |
| Config utils | `config/ConfigUtils.java` |

## CONVENTIONS
- `SMASHING_FACTORY_RECIPES` reads tier/voltage limits from config.
- Config is initialized from `common/CommonProxy.java`.

## ANTI-PATTERNS
- Do not read config values before config init.

## SCOPE
Applies to `src/main/java/com/mo_guang/ctpp/config`.

## READ WHEN
- Adding or changing CTPP config options.

## SOURCE OF TRUTH
- `config/` classes and `common/CommonProxy.java` init.

## WORKFLOW
1. Check config registration in `CommonProxy`.
2. Run `:modules:CTPP:build` after changes.