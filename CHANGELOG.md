# Changelog

## 0.2.3 - 2023-12-11

### :fist: Fixes

- Decouple `multi_value` and `multiple`.

SLOC Analysis:

| Directory        |   Empty |   Comment |   Docstring |   Code |   Statements |
|------------------|---------|-----------|-------------|--------|--------------|
| src/argparse_tui |     318 |       128 |         164 |   1693 |         1020 |
| tests            |      56 |         0 |          11 |    211 |          108 |

## 0.2.2 - 2023-10-29

### :fist: Fixes

- Type lookup when given a partial with kwargs [8c48e8c]
- Enforce proper handling of is_flag arguments [450cc5e]

### :point_right: Changes

- Use more generic type-hints [016d634]
- Pin textual < 1 [f17b432]

## 0.2.1 - 2023-08-24

### :point_right: Changes

- Derive root cmd name from parser.prog [52d6a65]
- Remove 'group' label [45dc5d4]

### :fist: Fixes

- Correct logic for required arguments [7e818a6]

## 0.2.0 - 2023-07-29

### :clap: Features

- Passthru command-line values to TUI form [4ed259f]

### :point_right: Changes

- *Breaking:* Remove support for mandatory prompts [76beab4]

---

## 0.1.3 - 2023-07-28

### :clap: Features

- Copy command to clipboard before running [1d03f57]

### :point_right: Changes

- `add_command` will now return the subparser [5fe982d]
- Suppress error if clipboard copy fails [6e00995]
- Rename example [bd245fe]

---

## 0.1.2 - 2023-07-24

### :clap: Features

- `invoke_tui` [554827b]

### :fist: Fixes

- Handle argparse.REMAINDER [5447b92]
- Positional arguments go after options in the generated command [0a91a2e]

---

## 0.1.1 - 2023-07-23

### :fist: Fixes

- Only accept root ArgumentParser in `add_tui_command` [6f124f0]
- Correct image name in docker-compose [bcbfcec]

---

## 0.1.0 - 2023-07-22

- Init fork as argparse-tui :rocket: [367bc96]

### :clap: Features

- Argparse support [394d4dc]
- Ctrl+y to copy command [99d24f2]
- Add hacker keybindings [262f231]
- Redact sensitive values [ca0df16]
- Support click prompt_required [48809bf]
- Omit hidden parameters and subcommands [0a7ed9d]
- Support typer [705e432]
- *Breaking:* Refactor to make click optional [91db7dd]

### :fist: Fixes

- Regain feature parity with trogon/main [ca15753]
- Fixed command info when no docstring is present [d434653]
- Fixed help_text if self.schema.help is none [f42f995]

### :point_right: Changes

- Generate `post_run_command` on-closed, not on-changed [afd8883]