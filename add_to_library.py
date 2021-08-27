from ytmusicapi import YTMusic
import argparse
import csv

yt = YTMusic('headers_auth.json')

parser = argparse.ArgumentParser()
parser.add_argument("input", type=str)
parser.add_argument('--dry-run', dest='dry_run', action='store_true')
parser.add_argument('--no-dry-run', dest='dry_run', action='store_false')
args = parser.parse_args()

def main():
    print(args.input)
    if (args.dry_run):
        playlistId = "test"
    else:
        playlistId = yt.create_playlist("Import 3", "imported song")

    with open(args.input) as albums:
        album_reader = csv.reader(albums, delimiter='\t')
        errors = []
        success = []
        for album in album_reader:
            print(album)
            if search_and_add(album, playlistId):
                success.append(album)
            else:
                errors.append(album)
        print("Success: ", len(success))
        print("Errors:")
        print(*errors)

def search_and_add(album, playlistId = None):
    results = yt.search(album[0] + " " + album[1], filter = "albums")
    added = False
    if results is not None:
        for result in results:
            result_title = str(result['title']).lower()
            ## break if this is really similar otherwise move to the next one.
            if (result_title.find(str(album[0]).lower()) != -1 or result_title.find(str(album[1].lower())) != -1):
                print(result['title'], " id: ", result['browseId'])
                trackIds = add_album(result['browseId'])
                if (not args.dry_run):
                    response = yt.add_playlist_items(playlistId, trackIds)
                else:
                    print("would have added ", len(trackIds), " to ", playlistId)
                added = True
                break
    return added


def add_album(albumId):
    album = yt.get_album(albumId)
    trackIds = []
    if (album is not None):
        ## loop through the tracks, add to library
        for track in album['tracks']:
            if not args.dry_run:
                if 'feedbackTokens' in track and track['feedbackTokens']['add']:
                    response = yt.edit_song_library_status(track['feedbackTokens']['add'])
                    if (not response['feedbackResponses'][0]['isProcessed']):
                        print("Error adding ", track['title'], " from ", album['title'])
            else:
                if 'feedbackToken' in track:
                    print("already have ", track['title'])
                elif 'feedbackTokens' in track:
                    print("would have added ", track['title'])
            trackIds.append(track['videoId'])
    return trackIds

main()