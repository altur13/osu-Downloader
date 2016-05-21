# osu-Downloader

osu! Downloader is a script to help download beatmaps from the osu! site.
This script works on two steps: first, the user must create a list of
beatmaps to download, via a search query to osusearch.com. After this
list is created, the user can start the download of beatmaps: the script
will download each beatmap from the created list.
The purpose of this script is to download beatmaps for archiving: if the
user has a slow connection and lots of beatmaps, is something happens
and the user must recreate the songs folder, it's best to have all the
osz files already downloaded and stored somewhere on disk. This is not
possible with downloads via direct.

## Commands and arguments

In this section all the script's commands and arguments will be explained.

### query

```
$ ./downloader.py query [QUERY_TERMS]
```

This command creates a list of beatmaps for dowload using osusearch.com
and a query entered by the user. The results is stored on a file named
`__query_results.txt` (TODO: make this a option for the user).

The following query terms are supported by this script:

```
title="big black"
artist="reol"
mapper="hollow wings"
source="beatmania"
diff_name="extra"
genres="anime,jpop"
languages="japanese,english"
status="ranked,qualified,unranked"
modes="standard,mania"
star_min="4.2"
ar_min="9"
order_by="favorites"
```

Ex: A query that searches for all ranked standard miiro maps...

```
$ ./downloader.py query title="miiro" artist="akino" modes="standard" status="ranked"
```

### update

As you must have noticed, there is no OR statement above. This is because the user
can issue a `update` to the query, to add more maps to the list. This command
is the same as the query command above: it receives a list of query terms and
access osusearch.com to retreive the list of beatmaps. The difference is that
the command above overwrites the list of beatmaps, while this command appends
the result to the list.

### check

```
$ ./downloader.py check [SOME_DIR]
```

This command makes a list of all .osz files present on `SOME_DIR` and then mark
these beatmaps as downloaded on the beatmap list, to prevent the program from
redownloading these beatmaps. This command is useful when the user has already 
downloaded some beatmaps.

### download

```
$ ./downloader.py download [SOME_DIR]
```

This is the command used to download beatmaps from the osu! website. It will dowload every beatmap on the list, with a interval of one minute between downloads. If the 
download was successful, it will mark the beatmap as DOWNLOADED; if it was not
successful, it will mark the beatmap as NOT AVAILABLE. After the download finishes,
the user can go through every NOT AVAILABLE beatmap and download the from
bloodcat manually (TODO: make the script do this...).
