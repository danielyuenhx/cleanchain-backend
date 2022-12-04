#!/usr/bin/env bash

# load variables from config file
source "$(dirname ${BASH_SOURCE[0]})/config.sh"

# select transaction
goal app call \
    --app-id "$APP_ID" \
    -f "$CLAIMANT_ACCOUNT" \
    --app-arg "str:select"


# deselect transaction
# goal app call \
#     --app-id "$APP_ID" \
#     -f "$CLAIMANT_ACCOUNT" \
#     --app-arg "str:deselect"

