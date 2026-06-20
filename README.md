# Commencement

we need ideas for content:

1. Anime clips?? (apparently might be no longer monetized)
2. Meme compilation (comptitive)
3. Lego timelapse (building scene from movie, then with AI making timelapse of same thing)
4. Clips from movies (Lego Movie, etc.) w/ Audio + Caption

FOR NOW:

Idea \#4: Clips from Lego Movie, add captions (manually), add audio... shoot.

Plan: 
- clip the video using Python
- add captions using Python (constant captions)
- figure out how to do audio
- connect the pieces
- get Google API
- connect to youtube
- at this point: run main.py: choose the clip (from folder), choose text (from folder), choose audio (folder?), spit out file. run upload.py: choose output file, uploads
- then: figure out automation method.

Update:
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