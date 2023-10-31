#!/bin/sh

help() {
    printf "usage: %s [board_url]\n" "$0" >&2
    printf "e.g. %s 'https://headline.5ch.net/bbynamazu/'\n" "$0" >&2
}

if [ -z "$1" ]; then
    help
    exit 1;
fi

echo "$1/subject.txt"
curl "$1/subject.txt" | iconv -f sjis -t utf8
