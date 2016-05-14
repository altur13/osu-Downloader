#!/usr/bin/env python3

import requests
import sys
import json
import os
import os.path

from osu_web_connection import *
from query import *
from beatmap import *

def query_osusearch(query):
    beatmap_list = []

    offset = 0
    while True:
        r = requests.get(query.get_query_string() + "offset=" + str(offset))
        result = json.loads(r.text)
        #print(result)
        if not result['beatmaps']:
            break
        else:
            for b in result['beatmaps']:
                beatmap = Beatmap()
                beatmap.build_from_query(b)
                beatmap_list.append(beatmap)
        offset += 1
    return beatmap_list


def build_query(args):
    query = OsuSearchQuery()
    for s in args:
        key, value = s.split('=')
        if key == "title":
            query.set_title(value)
        elif key == "artist":
            query.set_artist(value)
        elif key == "mapper":
            query.set_mapper(value)
        elif key == "source":
            query.set_source(value)
        elif key == "diff_name":
            query.set_diff_name(value)
        elif key == "genres":
            for s in value.split(','):
                query.add_genre(s)
        elif key == "languages":
            for s in value.split(','):
                query.add_language(s)
        elif key == "status":
            for s in value.split(','):
                query.add_status(s)
        elif key == "modes":
            for s in value.split(','):
                query.add_mode(s)
        elif key == "star_min":
            query.set_star_range(value)
        elif key == "ar_min":
            query.set_ar_range(value)
        elif key == "order_by":
            query.set_query_order(value)
        else:
            continue
    print(query.get_query_string())
    return query


def read_beatmap_list(file_name):
    beatmap_list = []
    if os.path.isfile(file_name):
        with open(file_name) as f:
            lines = f.readlines()
            for l in lines:
                if l.startswith('#'):
                    continue
                b = Beatmap()
                b.build_from_file_line(l)
                beatmap_list.append(b)
    return beatmap_list


def write_beatmap_list(beatmap_list, file_name):
    with open(file_name, "w+") as f:
        for b in beatmap_list:
            f.write(b.export_string() + "\n")


def check_download_status(path):
    beatmap_list = read_beatmap_list("__query_results.txt")
    beatmap_dict = {}  # to assist on the search for beatmap
    for b in beatmap_list:
        beatmap_dict[b.beatmapset_id] = b

    # builds file list
    l = os.listdir(path)
    l.sort()
    file_list = []
    for f in l:
        file_list.append(f.split(" ")[0])

    for bid in file_list:
        if bid in beatmap_dict.keys():
            print("Found " + bid + " on download dir...")
            beatmap_dict[bid].download_status = "DOWNLOADED"

    for b in beatmap_list:
        print(b.download_status + ": " + str(b.beatmapset_id) + " -> " + b.artist + " - " + b.title + " (by " + b.mapper + ")")

    write_beatmap_list(beatmap_list, "__query_results.txt")



def main(args):
    if args[0] == "query":
        print(os.getcwd())
        query = build_query(args[1:])
        beatmap_list = query_osusearch(query)
        for b in beatmap_list:
            b.print_info()
            print("")
        write_beatmap_list(beatmap_list, "__query_results.txt")
    elif args[0] == "check":
        if len(args) < 2 or not os.path.isdir(args[1]):
            print("Error: check directory not specified")
            exit(1)
        check_download_status(args[1])




if __name__ == "__main__":
    main(sys.argv[1:])
