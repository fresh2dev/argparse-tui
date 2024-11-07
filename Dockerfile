FROM python:3.13.0-slim-bullseye as build
RUN apt-get update \
    && apt-get install --upgrade -y git build-essential gcc libssl-dev libffi-dev python3-dev
WORKDIR /workspace
COPY . /workspace
ENV PYTHONUNBUFFERED=1
RUN python3 -m pip install 'mkdocs==1.*' \
    'mkdocs-material>=9.5,<10' \
    'mkdocs-jupyter' \
    'mkdocs-include-dir-to-nav' \
    'mkdocstrings[python]' \
    'black' \
    'mkdocs-autorefs' \
    'pymdown-extensions' \
    'pygments'

RUN python3 -m mkdocs build -d public

FROM nginx:1
COPY --from=build /workspace/public /usr/share/nginx/html
