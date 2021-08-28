from ytmusicapi import YTMusic
import argparse
import csv
import re

SOUNDTRACK_ARTISTS = {'various artists'}
SOUNDTRACK_ALBUMS_REGEX = re.compile(r"original.*[soundtrack|recording]")

def main():
    yt = YTMusic('headers_auth.json')

    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str)
    parser.add_argument("playlist", type=str)
    parser.add_argument('--dry-run', dest='dry_run', action='store_true')
    parser.add_argument('--no-dry-run', dest='dry_run', action='store_false')
    args = parser.parse_args()

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
            if search_and_add(yt, album, playlistId, dryRun):
                success.append(album)
            else:
                errors.append(album)
        print("Success: ", len(success))
        print("Errors:")
        print(*errors)

def search_and_add(yt, album, playlistId = None, dryRun = False):
    results = yt.search(album[0] + " " + album[1], filter = "albums")
    added = False
    if results is not None:
        for result in results:
            ## break if this is really similar otherwise move to the next one.
            if (is_album_match(album[0], album[1], result)):
                print(result['title'], " id: ", result['browseId'])
                trackIds = add_album(yt, result['browseId'], dryRun)
                if (not dryRun):
                    response = yt.add_playlist_items(playlistId, trackIds)
                else:
                    print("would have added ", len(trackIds), " to ", playlistId)
                added = True
                break
    return added

def is_album_match(artist, album, result):
    artist = artist.lower()
    album = album.lower()
    result_title = str(result['title']).lower()

    if is_soundtrack(artist, album):
        ## be more stringent: make sure the unique string is the first
        unique_str = album if artist in SOUNDTRACK_ARTISTS else artist
        return result_title.find(unique_str) == 0
    else:
        return result_title.find(album) != -1 or result_title.find(artist) != -1

def is_soundtrack(artist, album):
    artist = artist.lower()
    album = album.lower()
    return artist in SOUNDTRACK_ARTISTS or SOUNDTRACK_ALBUMS_REGEX.match(album) is not None

def add_album(yt, albumId, dryRun = False):
    album = yt.get_album(albumId)
    trackIds = []
    if (album is not None):
        ## loop through the tracks, add to library
        for track in album['tracks']:
            if not dryRun:
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

if __name__ == '__main__':
    main()
