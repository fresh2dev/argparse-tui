# Changelog

## 0.1.3 - 2023-07-28

### :clap: Features

- Copy command to clipboard before running [1d03f57]
- `add_command` will now return the subparser [5fe982d]

### :point_right: Changes

- Suppress error if clipboard copy fails [6e00995]
- Rename example [bd245fe]

## [0.1.2] - 2023-07-24

### :clap: Features

- `invoke_tui` [554827b]

### :fist: Fixes

- Handle argparse.REMAINDER [5447b92]
- Positional arguments go after options in the generated command [0a91a2e]

## [0.1.1] - 2023-07-23

### :fist: Fixes

- Only accept root ArgumentParser in `add_tui_command` [6f124f0]
- Image name in docker-compose [bcbfcec]

### :metal: Other

- 0.1.0 --> 0.1.1 [2dbb5b6]

## [0.1.0] - 2023-07-22

### :clap: Features

- Ctrl+y to copy command [99d24f2]
- Add hacker keybindings [262f231]
- Argparse support [394d4dc]
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

- Init fork as argparse-tui [367bc96]
- Generate `post_run_command` on-closed, not on-changed [afd8883]

### :shit: Unconventional

- Version bump
 [25eab1e]
- Ensure custom command names dont appear in sidebar
 [163d7e1]
- Expect at least one space
 [c93fa7f]
- Removed double period, looked weird
 [40716a4]
- Docs for tui(help=, command=), refs #2
 [ec63d61]
- @tui(help=, command=) parameters, refs #2
 [2465e00]
- Bump version
 [3030835]
- Styles
 [c52b78d]
- Version bump
 [d80921f]
- Polyfill for orig_argv
 [2197a70]
- Remove examples
 [f7fdd58]
- Add highlighting, remove some examples
 [78fcf93]
- Highlighting the help text
 [178d5bf]
- Initial search implementation
 [1ab7645]
- Fix pytest command in CI
 [8ce80d7]
- Dont try to install dev extras
 [0303f45]
- Fix github directory structure
 [30135a3]
- Add GitHub Actions
 [f46351c]
- Add support for nargs=-1
 [788d022]
- Remove redundant comment
 [9107e4a]
- Detecting the run string, remove debugging
 [d2557cc]
- Add support for custom ParamType subclasses
 [c04c875]
- Increase count option value limit to 5
 [61e78c6]
- Remove unused method, fixed tests
 [25a753b]
- Fix no args commands not showing, fix default arguments when using groups
 [204c8a5]
- Fix typos

Found via `codespell`.
 [dc9ca70]
- Remove dist files
 [55e2bb6]
- Update README.md [b9ddd90]
- Update README.md [627a304]
- Update README.md [6a2d748]
- Fix assets [27be2e3]
- Update README.md [fb4e51d]
- Update README.md [d3ea8fe]
- Fixes
 [a764944]
- Update README.md [0752be2]
- Update README.md [d3945f6]
- Update README.md [c471ed2]
- Gitignore
 [185047b]
- Version bump
 [f7adc20]
- Version bump
 [5293d3c]
- Update README.md [79cfd5e]
- Update README.md [1e85196]
- Update README.md [4b83410]
- Update README.md [86015ea]
- Update README.md [55c3957]
- Update README.md [3e0186a]
- Update README.md [020c69a]
- Update README.md [4574dfb]
- Update README.md [dedf036]
- Update README.md [383dd99]
- Update README.md [a205719]
- Version bump
 [435c224]
- Tweaks, fix verbosity
 [0068501]
- Changes, tweaks, fixes
 [b29078d]
- Tweaks and fixes
 [4b0f162]
- Add quick README
 [1573743]
- Formatting
 [bca1625]
- Showing min and max range
 [16a1bda]
- Add support for counting options (e.g. -vv)
 [d9963f7]
- Styling change
 [310d8a1]
- Add metadata tab
 [5a81626]
- Command info and metadata tab, but metadata not yet implemented
 [62eacf5]
- Add command info popup
 [ca29e86]
- Placeholder for command info modal
 [70870c8]
- Reverse display of commands in form from path to root
 [85753d2]
- Small UI tweak
 [eb5366f]
- Text placeholders show default values
 [eff1ab3]
- Various bits of polish
 [cbf9169]
- Fix recursion issue with building the command from the tree
 [40ff493]
- Ensure nargs=-1 is supported, fix layout when add another is clicked and only a single widget is added
 [c4ae97a]
- Fixing button position, ensuring command scrolls if it gets too big
 [6052b6a]
- Only display placeholder in CLI exec string if required
 [94b5ef0]
- Ensuring checkbox labels arent double rendered
 [4c230ea]
- Dont do group rendering when only a single widget is in a group
 [01f6bb5]
- Fix tab focusing issue
 [d2dee99]
- Fix command buildiing in grouped CLIs
 [3cba021]
- Fixing default value detection
 [48944e1]
- Some styling fixes
 [5d2c9bd]
- Make multiple choice work like radioset with arrow keys
 [ac1defc]
- Remove placeholders
 [28386ee]
- Tracking first control, layout fix
 [ffdfed3]
- Support for boolean flag pairs
 [40277f7]
- Ensure defaults load into MultipleChoice correctly
 [6d71f3c]
- Ensure defaults loaded into radioset correctly
 [1001b91]
- Fixing default values displays
 [af4febb]
- More display changes
 [2cd0d50]
- Better display for missing parts of multi-value options
 [eec7e40]
- Logic for non-supplied values
 [c67919c]
- Fix logic for default values
 [1be7b30]
- Bug fixes
 [dce9e67]
- Ensure we process collected values as multivalues
 [10cc856]
- Fix formatting
 [3f3dc4a]
- Create and use wrapper class ensuring param format consistent
 [0f5981b]
- Updating get_values
 [bcfc1c0]
- Styling fixes
 [8197874]
- Use new Textual `@on` decorator
 [e066a5e]
- Support root level options, add demo app, tidy up
 [61da3d6]
- Ensure the root click group is added to the tree
 [a97eca4]
- Working on getting MultipleChoice values correctly
 [5268d54]
- Mostly building up the commands to support multiple True and multi-value
 [dc39640]
- Ability to add instances of the widget groups
 [e971ad8]
- Fix interaction between defaults/multiple=True/multi-value options
 [7857066]
- Begin refactor for multi-value multiple options
 [427ef52]
- Extracting common logic for rendering form controls
 [e1f9675]
- Refactoring to prepare for multi-value widgets
 [e4da215]
- Sort the options in the column
 [26cf197]
- Thinner scrollbars in the tree
 [b808b4e]
- Minor fixes and UI updates
 [52c5156]
- Tidying up some code, show all option variants
 [a4d7ffd]
- Make multiple text input work
 [b0ae20c]
- Begin support for multiple text, run with exec, wire up the cutton
 [b2a07cc]
- Applying gitignore
 [e421c39]
- Make defaults with multiple choice interact correctly
 [ae37bcc]
- Add support for default choice
 [0eb29e5]
- Support for multiple-choice options
 [369cc58]
- Formatting, improving display of param inheritance
 [212230b]
- UI showing when params belong to parent
 [218bbb1]
- Hide defaults properly, dim groups in the tree
 [f6d25e4]
- Building command correctly for both group and non-group case
 [4118b14]
- Tidy up root command prefixing
 [daa5116]
- Including correct root command in the preview
 [77e1974]
- Add highlighting to command preview
 [e8128fd]
- Fix path argument types, using AwaitMount where required
 [46d4f19]
- Ensure form is correctly processed when tree node highlight changes
 [7d21d67]
- Only display command tree when it makes sense
 [f353a1d]
- Extracting widgets into files, hiding empty groups
 [5151fe3]
- Adding help text
 [f7d6a5f]
- Ensure choices are correctly populated for click.Option
 [a4bfb55]
- Correctly building command, launching TUI as a subcommand
 [01b3ccd]
- Improve a comment
 [2182f10]
- Add note on how we are going to build up the command
 [15541e6]
- Small display improvements, bugfixes
 [4cf0c7c]
- Form rendering supports parent commands/groups that have their own options
 [bb77a58]
- Remove validation, sketching out approach for linking form controls to schema
 [62b3499]
- Dont worry about validation for now
 [18b56fc]
- Tidying tests
 [45d0692]
- Add some testsgs
 [1752465]
- Some renaming, refactoring
 [1b3e198]
- Formatting
 [9be5303]
- Validating input against schema
 [3ddf9da]
- Showing help text in placeholder
 [8a8acff]
- Displaying radiosets and checkboxes when the type is appropriate
 [2b95bd5]
- Formatting and fixing typing
 [f4eb3dd]
- Running command on exit
 [83742e3]
- Rewrite to use dataclasses
 [f273d19]
- Update docstring and type hint
 [83cff92]
- Using TypedDict instead of dict for command schema
 [ecc091c]
- Tidying up the form
 [ca2f4ae]
- Make layout more sensible
 [c10971b]
- Adding execute button to command preview
 [8f6e300]
- Include the choices when the type is click.Choice
 [12812f9]
- Execution string preview
 [82b321e]
- Refactor to use screens, tidying up code
 [e30c49b]
- Styling command tree
 [1a6a408]
- Passing in an app name
 [0c87625]
- Make home body focusable
 [a714998]
- Layout improvements
 [be808d1]
- Skeleton with sidebar and introspection
 [73e8180]
- Initial commit
 [09eff5b]

<!-- generated by git-cliff -->
