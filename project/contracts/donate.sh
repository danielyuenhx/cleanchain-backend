#!/usr/bin/env bash

# load variables from config file
source "$(dirname ${BASH_SOURCE[0]})/config.sh"

# create donate transaction
goal app call \
    --app-id "$APP_ID" \
    -f "$DONOR_ACCOUNT" \
    --app-arg "str:donate" \
    --app-arg "str:$DONATION" \
    -o donate-call.tx 
#output the transaction to a file instead of sending it
#to the network since only a group of 2 transactions
#is accepted


# create donation transaction
goal clerk send \
    -a "$DONATION" \
    -t "$APP_ACCOUNT" \
    -f "$DONOR_ACCOUNT" \
    -o donate-amount.tx

# group transactions
cat donate-call.tx donate-amount.tx > donate-combined.tx
goal clerk group -i donate-combined.tx -o donate-grouped.tx
goal clerk split -i donate-grouped.tx -o donate-split.tx

# sign individual transactions
goal clerk sign -i donate-split-0.tx -o donate-signed-0.tx
goal clerk sign -i donate-split-1.tx -o donate-signed-1.tx

# re-combine individually signed transactions
cat donate-signed-0.tx donate-signed-1.tx > donate-signed-final.tx

# send transaction
goal clerk rawsend -f donate-signed-final.tx 
#goal clerk dryrun -t donate-signed-final.tx --dryrun-dump -o dr.msgp