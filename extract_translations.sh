#!/bin/sh
pybabel extract \
    -F babel.ini \
    --project "slap" \
    --msgid-bugs-address dev@local \
    --copyright-holder dev \
    --version 0.1 \
    -o messages.pot \
    .
pybabel update \
    -i messages.pot \
    -d translations
