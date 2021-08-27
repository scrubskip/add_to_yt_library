from ytmusicapi import YTMusic
import argparse
import csv

yt = YTMusic('headers_auth.json')

parser = argparse.ArgumentParser()
parser.add_argument("input", type=str)
parser.add_argument("dry_run", type=bool)
args = parser.parse_args()

def main():

    print(args.input)
    with open(args.input) as albums:
        album_reader = csv.reader(albums, delimiter='\t')
        errors = []
        success = []
        for album in album_reader:
            print(album)
            if search_and_add(album):
                success.append(album)
            else:
                errors.append(album)
        print("Success: ", len(success))
        print("Errors:")
        print(*errors)

def search_and_add(album):
    results = yt.search(album[0] + " " + album[1], filter = "albums")
    added = False
    if results is not None:
        for result in results:
            result_title = str(result['title']).lower()
            ## break if this is really similar otherwise move to the next one.
            if (result_title.find(str(album[0]).lower()) != -1 or result_title.find(str(album[1].lower())) != -1):
                print(result['title'], " id: ", result['browseId'])
                add_album(result['browseId'])
                added = True
                break
    return added


def add_album(albumId):
    album = yt.get_album(albumId)
    if (album is not None):
        ## loop through the tracks, add to library
        for track in album['tracks']:
            if not args.dry_run:
                response = yt.edit_song_library_status(track['feedbackTokens']['add'])
                if (not response['feedbackResponses'][0]['isProcessed']):
                    print("Error adding ", track['title'], " from ", album['title'])
            else:
                print("would have added ", track['title'])

main()