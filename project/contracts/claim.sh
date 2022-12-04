#!/usr/bin/env bash

# load variables from config file
source "$(dirname ${BASH_SOURCE[0]})/config.sh"

# create select transaction
goal app call \
    --app-id "$APP_ID" \
    -f "$CLAIMANT_ACCOUNT" \
    --app-arg "str:claim" \
    --app-arg "str:40" \
    --dryrun-dump -o dryrun.msog