# 2ch.sh

2ch browser based on UNIX philosophy.

UNIX哲学に基づいた2ちゃんねる専用ブラウザ

## requirement

- POSIX compatiple OS
- curl
- python
  - to make bbsmenu usable

## install

```shell-session
mkdir -p $XDG_CACHE_HOME/2ch.sh
```

git clone & cd

## usage

### 板一覧を取得する

```shell-session
curl menu.5ch.net/bbsmenu.html | iconv -f sjis -t utf8 | python contrib/mkbbsmenu.py
```

### 板にあるスレタイを取得する

```shell-session
getsubject {板のURL}
```

fzfなどのfuzzy finderを使えばスレタイから検索できます

```shell-session
getsubject {板のURL} | fzf
```

さらにfzfは選択した行を出力するので、結果を加工することでスレを読むこともできます（対応予定）

### スレを読む

```shell-session
getdat $THREAD_URL
```

読みやすい形に変換してlessなどのpagerで読むと読みやすいです:

```shell-session
getdat $THREAD_URL | parsedat | less
```
