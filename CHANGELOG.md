# Changelog

## 0.1.2 - 2023-07-24

### :clap: Features

- `invoke_tui` [b6b3367]

### :fist: Fixes

- Handle argparse.REMAINDER [3cb78b6]
- Positional arguments go after options in the generated command [4e3bfbf]

## 0.1.1 - 2023-07-23

### :fist: Fixes

fix: only accept root ArgumentParser in `add_tui_command`

## 0.1.0 - 2023-07-23

### :clap: Features

- Init fork as argparse-tui [6cdffc6]
- Argparse support [394d4dc]
- Refactor to make click optional [91db7dd]
- Redact sensitive values [ca0df16]
- Add hacker keybindings [262f231]
- Ctrl+y to copy command [99d24f2]
- Omit hidden parameters and subcommands [0a7ed9d]

### :fist: Fixes

- Fixed command info when no docstring is present [d434653]
- Fixed help_text if self.schema.help is none [f42f995]

### :point_right: Changes

- Generate `post_run_command` on-closed, not on-changed [afd8883]
