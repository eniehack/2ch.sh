#!/bin/sh

usage() {
    printf "get dat from url\n" >&2
    printf "usage: %s [dat_url]\n" "$0" >&2
}

if [ -z "$1" ]; then
    usage
    exit 1;
fi

CACHEDIR="${XDG_CACHE_HOME:-$HOME/.cache}/2ch.sh"
DIR="$(echo "$1" | sed 's/https:\/\///' | sed 's/\/dat//')"

curl "$1" | iconv -f sjis -t utf-8 > "$CACHEDIR/$DIR"
cat "$CACHEDIR/$DIR"
