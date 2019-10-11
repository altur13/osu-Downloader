#!/usr/bin/env python3

import requests
import sys
import json
import os
import os.path
import time

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
        elif key == "min_length":
            query.set_min_length(value)
        elif key == "max_length":
            query.set_max_length(value)
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
    filtered = [x for x in l if x.endswith(".osz")]
    file_list = []
    for f in filtered:
        file_list.append(f.split(" ")[0])

    for bid in file_list:
        if bid in beatmap_dict.keys():
            print("Found " + bid + " on download dir...")
            beatmap_dict[bid].download_status = "DOWNLOADED"

    for b in beatmap_list:
        print(b.download_status + ": " + str(b.beatmapset_id) + " -> " + b.artist + " - " + b.title + " (by " + b.mapper + ")")

    write_beatmap_list(beatmap_list, "__query_results.txt")


def perform_query(query_string):
    query = build_query(query_string)
    beatmap_list = query_osusearch(query)
    for b in beatmap_list:
        b.print_info()
        print("")
    return beatmap_list

def update_stored_results(new_query_results, file_path):
    stored_results = read_beatmap_list(file_path)
    beatmap_dict = {}
    for b in stored_results:
        beatmap_dict[b.beatmapset_id] = b

    for n in new_query_results:
        if n.beatmapset_id not in beatmap_dict.keys():
            print("New beatmap " + str(n.beatmapset_id) + "...")
            stored_results.append(n)
    write_beatmap_list(stored_results, "__query_results.txt")

def download_beatmap_list(download_list, download_dir):
    conn = OsuWebConnection()
    abs_path = os.path.abspath(download_dir)
    stored_results = read_beatmap_list(download_list)
    not_downloaded = [b for b in stored_results if b.download_status == "NOT DOWNLOADED"]
    counter = 0
    for b in not_downloaded:
        conn.download_beatmap(b, abs_path)
        write_beatmap_list(stored_results, download_list)
        if b.download_status == "DOWNLOADED":
            print("Waiting 10 secs for next download...")
            time.sleep(10)
        counter += 1
        print(str(counter) + "/" + str(len(not_downloaded)) + " downloaded")
    conn.close()


def main(args):
    if args[0] == "query":
        print(os.getcwd())
        query_results = perform_query(args[1:])
        write_beatmap_list(query_results, "__query_results.txt")
    elif args[0] == "check":
        if len(args) < 2 or not os.path.isdir(args[1]):
            print("Error: check directory not specified")
            exit(1)
        check_download_status(args[1])
    elif args[0] == "update":
        query_results = perform_query(args[1:])
        update_stored_results(query_results, "__query_results.txt")
    elif args[0] == "download":
        if len(args) < 2 or not os.path.isdir(args[1]):
            print("Error: download directory not found")
            exit(1)
        download_beatmap_list("__query_results.txt", args[1])





if __name__ == "__main__":
    main(sys.argv[1:])
