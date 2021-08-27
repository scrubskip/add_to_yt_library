from ytmusicapi import YTMusic
import argparse
import csv

ytmusic = YTMusic('headers_auth.json')

parser = argparse.ArgumentParser()
parser.add_argument("input", type=str)
args = parser.parse_args()

print(args.input)
with open(args.input) as albums:
    album_reader = csv.reader(albums, delimiter='\t')

    for album in album_reader:
        print(album)