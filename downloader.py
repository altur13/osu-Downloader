#!/usr/bin/env python3

import requests
import sys
import json
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
                beatmap.title = b['title']
                beatmap.beatmap_id = b['beatmap_id']
                beatmap.artist = b['artist']
                beatmap.mapper = b['mapper']
                beatmap.bpm = b['bpm']
                beatmap.add_status(b['beatmap_status'])
                beatmap.length = b['total_length']
                beatmap.favorites = b['favorites']
                beatmap.diff_name = b['difficulty_name']
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
                beatmap_list.append(b.self_build(l))
    return beatmap_list


def write_beatmap_list(beatmap_list, file_name):
    with open(file_name, "w+") as f:
        for b in beatmap_list:
            f.write(b.export_string() + "\n")


def main(args):
    if args[0] == "query":
        print(os.getcwd())
        query = build_query(args[1:])
        beatmap_list = query_osusearch(query)
        for b in beatmap_list:
            b.print_info()
            print("")
        write_beatmap_list(beatmap_list, "__query_results.txt")


if __name__ == "__main__":
    main(sys.argv[1:])
