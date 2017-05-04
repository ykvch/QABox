#!/usr/bin/env bash

URL="https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"
PROXY=""  # optional "http://proxy.host:port"
WATCH_DIR="/tmp"
PATTERN="*.core"
TIMEOUT=30  # seconds, limits frequency of reports

HOST=`hostname`
LAST_TS=0
COUNTER=0

function send_report()
{
    if [ -n $PROXY ]; then
        proxy_param="-x "$PROXY
    fi

    user=$1
    fname=$2
    text="Core $fname triggered by @$user on $HOST"
    data='{"text": "'$text'"}'
    curl $proxy_param -sH "Content-type: application/json" -d "$data" $URL
}


inotifywait -mqe create $WATCH_DIR |
while read path options name; do
    if [[ $name = $PATTERN ]]; then
        ts=`date +%s`
        if [ $(($ts-$LAST_TS)) -ge $TIMEOUT ]; then
            user=`ls -ld $path$name | awk '{print $3}'`
            send_report $user $path$name $COUNTER
            COUNTER=0
            LAST_TS=$ts
        else
            ((COUNTER++))
        fi
    fi
done
