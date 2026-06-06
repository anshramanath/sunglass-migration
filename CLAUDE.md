# CLAUDE.md

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

---

## Project Context: final-migration

This repo migrates WooCommerce product catalogues into a Supabase-backed multi-brand platform. Active work lives in `final-migration/`. Ignore `old-migration/` and `new-migration/` — they are abandoned.

### Key conventions
- Brand is set via the `BRAND` env var (e.g. `BRAND=prosport`). All scripts read this at runtime via `config/`.
- Pipeline scripts live in `final-migration/pipeline/`. Run them from the repo root.
- Output data lands in `final-migration/data/{brand}/` and is gitignored.
- Veeqo inventory is sourced from a local CSV (`pipeline/sellables_export*.csv`), not the API.
- Checks accumulate per entity — a product collects all failures before being flagged. One failure is enough to flag it.
- Variable products: SKU is null at product level; checks (Veeqo, SKU structure) apply at variation level only.
- Simple products: SKU, Veeqo presence, SKU structure, and non-empty variations array are all checked at fetch time.
- Bad variations (not in Veeqo or not an object) are dropped silently. A variable product needs at least 2 surviving variations to proceed.

### DB
Schema is in `final-migration/db/001_initial_schema.sql`. Field names in the pipeline use camelCase; DB columns use snake_case — the import step handles the mapping.
