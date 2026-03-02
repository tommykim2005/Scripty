# Rename: WizBot → Scripty

## Overview

All occurrences of `WizBot` in the codebase have been renamed to `Scripty`.

## Files Modified

| File | Line | Before | After |
|------|------|--------|-------|
| `README.md` | 1 | `# WizBot` | `# Scripty` |
| `gui/main_gui.py` | 11 | `root.title("WizBot GUI")` | `root.title("Scripty GUI")` |

## Search Coverage

The full codebase was searched (all `.py`, `.md`, `.json`, `.yaml`, `.toml`, `.cfg`, `.txt`, `.sh` files and filenames) for all case variants (`wizbot`, `WizBot`, `WIZBOT`, `wiz_bot`, etc.). Only the two occurrences above were found.

## Verification

- Post-rename grep confirms **0 remaining occurrences** of `wizbot` in any form.
- All Python source files (`main.py`, `gui/main_gui.py`, `utils/*.py`) pass `python3 -m py_compile` with no errors.
- No automated test suite exists in this project; no tests to run.

## Follow-up Notes

- **Git history**: Prior commit messages (`"Add README for WizBot automation toolkit"`, `"Initial commit for wizBot project"`) still reference the old name. Git history is intentionally left unchanged; the new commit message documents this rename.
- **Branch name**: The working branch `agent/scripty/refactor/rename-wizbot-to-scripty` already reflects the new name.
- If any external documentation, Discord bot configuration, or deployment scripts outside this repo reference `WizBot`, those should be updated separately.
