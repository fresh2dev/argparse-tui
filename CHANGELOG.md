# Changelog

All notable changes to this project will be documented in this file.

## 0.3.1 - 2024-11-26

**Full Changelog**: https://github.com/fresh2dev/argparse-tui/compare/0.3.0...0.3.1

### :fist: Fixes

- Weird characters shown on launch
- Better detection of `<secret>` flag in argument help

## 0.3.0 - 2024-11-07

**Full Changelog**: https://github.com/fresh2dev/argparse-tui/compare/0.2.6...0.3.0

### :clap: Features

- Add ability to open TUI with focus on a nested subcommand

### :point_right: Changes

- *Breaking* - Require python >= 3.9

## 0.2.6 - 2024-10-23

> This release cherry-picks several upstream fixes introduced in [Trogon v0.6.0](https://github.com/Textualize/trogon/releases/tag/v0.6.0)

**Full Changelog**: https://github.com/fresh2dev/argparse-tui/compare/0.2.5...0.2.6

### :fist: Fixes

- Fixing typing issues, ensure \*args and \*\*kwargs are passed to App superclass to help compatibility. Use `get_default_screen` instead of pushing a screen on_mount.
- Fix crashes on modern Textual, involving minor refactors
- Do not treat Select.BLANK as a supplied value

### :point_right: Changes

- Minimum Python version is now 3.8.1
- Update textualize dependency spec

## 0.2.5 - 2024-09-08

**Full Changelog**: https://github.com/fresh2dev/argparse-tui/compare/0.2.4...0.2.5

### :fist: Fixes

- Properly format text in 'about' widget
- Prefix binding actions with app namespace
- Tweak the styling to make the sidebar less greedy
- Allow functions to be used as arg types

### :metal: Other

- bump: Textual 0.54

## 0.2.4 - 2023-12-12

### :clap: Features

- `build_tui` and moar tests

### :fist: Fixes

- Regression introduced in 0.2.3

## 0.2.3 - 2023-12-11

### :fist: Fixes

- Decouple `multi_value` and `multiple`.

## 0.2.2 - 2023-10-29

### :fist: Fixes

- Type lookup when given a partial with kwargs \[8c48e8c\]
- Enforce proper handling of is_flag arguments \[450cc5e\]

### :point_right: Changes

- Use more generic type-hints \[016d634\]
- Pin textual \< 1 \[f17b432\]

## 0.2.1 - 2023-08-24

### :point_right: Changes

- Derive root cmd name from parser.prog \[52d6a65\]
- Remove 'group' label \[45dc5d4\]

### :fist: Fixes

- Correct logic for required arguments \[7e818a6\]

## 0.2.0 - 2023-07-29

### :clap: Features

- Passthru command-line values to TUI form \[4ed259f\]

### :point_right: Changes

- *Breaking:* Remove support for mandatory prompts \[76beab4\]

______________________________________________________________________

## 0.1.3 - 2023-07-28

### :clap: Features

- Copy command to clipboard before running \[1d03f57\]

### :point_right: Changes

- `add_command` will now return the subparser \[5fe982d\]
- Suppress error if clipboard copy fails \[6e00995\]
- Rename example \[bd245fe\]

______________________________________________________________________

## 0.1.2 - 2023-07-24

### :clap: Features

- `invoke_tui` \[554827b\]

### :fist: Fixes

- Handle argparse.REMAINDER \[5447b92\]
- Positional arguments go after options in the generated command \[0a91a2e\]

______________________________________________________________________

## 0.1.1 - 2023-07-23

### :fist: Fixes

- Only accept root ArgumentParser in `add_tui_command` \[6f124f0\]
- Correct image name in docker-compose \[bcbfcec\]

______________________________________________________________________

## 0.1.0 - 2023-07-22

- Init fork as argparse-tui :rocket: \[367bc96\]

### :clap: Features

- Argparse support \[394d4dc\]
- Ctrl+y to copy command \[99d24f2\]
- Add hacker keybindings \[262f231\]
- Redact sensitive values \[ca0df16\]
- Support click prompt_required \[48809bf\]
- Omit hidden parameters and subcommands \[0a7ed9d\]
- Support typer \[705e432\]
- *Breaking:* Refactor to make click optional \[91db7dd\]

### :fist: Fixes

- Regain feature parity with trogon/main \[ca15753\]
- Fixed command info when no docstring is present \[d434653\]
- Fixed help_text if self.schema.help is none \[f42f995\]

### :point_right: Changes

- Generate `post_run_command` on-closed, not on-changed \[afd8883\]
