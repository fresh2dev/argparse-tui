pub_dir := 'public'
assets_path := pub_dir + '/r/argparse-tui'

default:
    @ just --choose

[positional-arguments]
docs-dev:
    mkdocs serve --open "$@"

docs-build:
    rm -rf "{{pub_dir}}" \
    && mkdir -p "{{assets_path}}" \
    && mkdocs build -d $(mktemp -d) \
    && mv $_/* "{{assets_path}}" \

docs-upload: docs-build
    wrangler versions upload --no-bundle --cwd "{{pub_dir}}" --assets .

docs-publish: docs-build
    wrangler deploy --no-bundle --cwd "{{pub_dir}}" --assets .
