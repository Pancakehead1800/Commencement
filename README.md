# Commencement

## we need ideas for content:

1. Anime clips?? (apparently might be no longer monetized)
2. Meme compilation (comptitive)
3. Lego timelapse (building scene from movie, then with AI making timelapse of same thing)
4. Clips from movies (Lego Movie, etc.) w/ Audio + Caption

## FOR NOW:

## Idea \#4: Clips from Lego Movie, add captions (manually), add audio... shoot.

## Plan: 
- clip the video using Python
- add captions using Python (constant captions)
- figure out how to do audio
- connect the pieces
- get Google API
- connect to youtube
- at this point: run main.py: choose the clip (from folder), choose text (from folder), choose audio (folder?), spit out file. run upload.py: choose output file, uploads
- then: figure out automation method.

## Update:
- Instead of just movie clips, we need to find SOURCES
- once we find sources, we make the script to DOWNLOAD THEM
    - we will need to learn `os' library and other nonsense
    - How will we store them? in a raw_memes folder
- After we download the clips, we need to do OUR edits to them
    - Add our face (+eyepatch)??
    - Turn black background -> blurred overlay
    - NEED to add edits btw
    - Sal-style: shrink the meme, add background, add face
- Store results: final_outputs folder
- THEN: we need to figure out Google Oauth.... puhp
- THEN: debug
- THEN: debug
- THEN: debug
- THEN: debug
- THEN: debug
- THEN: debug
- THEN: debug
- THEN: we wait


## Update on certain details:
- Use r/dankmemes (golden)
- Have the face + background + music approach
- Use Synology + Docker to run containers i think?
    1. We manually download memes to a folder (on computer)
    2. Make scheduled task to run a container to randomly choose meme, add face, add music, and background, and format
    3. Then make task to randomly choose a finalized video to post to Youtube shorts

## Another update:
- We have the main editing working, BUT:
    1. We need MEMES (easy)
    2. We need MUSIC (tedius, ok)
    3. We need FACES (difficult: use Max + Cocoa once Immich loads, but need to remove bg)
    4. We need BACKGROUNDS (easy-ish, but need to compress)
- After all that, we need:
    1. Run it a few times
    2. Make uploading script
    3. Figure out how to get it constantly running
    4. Start uploading
We have 2 decent videos already, and once we get 12 that'll give us (12 x 6 hours = 72 hours =) 3 days to make more.
Of course, we will eventually want to decrease the upload rate to 1 every 4 hours, and none during the night.
Some more upgrades:
1. Every 4 hours -> Every 4 hours +/- 15 minutes
2. Prevent duplicate uploads (change data objects in data.json) and Even out file usage
3. Not sures


# Sources

## Memes:
1. https://pixabay.com/music/search/classical/

## Music:
1. https://pixabay.com/music/search/classical/
2. Arabeqsue recording

Need to acquire:
1. Laputa (the girl who fell from the sky)
2. First Suite (all 3)
3. ADD m4a SUPPORT!!!

## Backgrounds:
1. https://www.videezy.com/free-video/sunset

## Faces:
1. No clue where i got the cat one
2. Immich => ma DAWGS
