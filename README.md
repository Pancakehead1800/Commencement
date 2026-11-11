
# Project Commencement

### My Motivations

If you've ever seen an MIT Maker Portfolio on YouTube, you would know that high schoolers can produce very, *very* impressive work. I cannot. The best I have done thus far is a simple multi-neighbor cellular automata with `pygame` and `numpy`, and no, it is not as impressive as its complex name might suggest. Rather, I most enjoy doing simply, quick projects that are fun and rewarding. Hence the abundance of `pygame` projects: they usually give cool visuals that I like. This project is not like that.

I am in desperate need of money or a job. Other people make money, but I am too lazy. Thus, when I heard about someone making nearly 5k a month by creating a program to automatically create YouTube Shorts, I was intrigued. With 5k a month, I could:
1. Acquire a fancy computer
2. Buy gifts for others using my own money
3. Invest in other interests (such as computer engineering with an Arduino kit)
4. Not feel the guilt of dependency.

Thus, wanting to build something more meaningful, and blinded by the greed of a very wishful source of money, I began this project. In the end, it ended up being slightly more than another small project though. lol.


### Introduction

So what is this project? It's very simple. Running the ... `main.py` script ... i think ... will automatically create a YouTube Short and upload it. However, you must first acquire some data/files. There are four file types to gather (for the videos) 

1. Background files (I used `.mp4` files of a sunset) for the background of the short.
2. Face files (I found some `.png` pictures of my dawgs, then ran the `converts.py` file ... i think ... to get rid of the backgrounds).
3. Content files (I used memes from reddit. They can be `.jpg`, `.png`, or `.mp4`)
4. Music files (literally just `.mp3` files)

Furthermore, you need to collect some secret keys (for uploading to YouTube--you can skip this part if you're willing to upload manually). Honestly, I forgot how I did this, but you can probably ask AI.

Lastly ... I'm pretty sure there's something else ... maybe not!

The program does take some computational power to execute, as it has to create compile each frame using the files given, but it isn't too bad.

Additionally, you can change certain constants (like video length) in the `constants.py`


### How it works

Honestly I don't remember all the details. I know it uses some media-editing packages--check `requirements.txt` for the full list. Also, there is a `dockerfile` and `compose.yaml`, so if you every need to run it on a server (like run it every few days or every few hours), and if you can figure out how to use `Docker` (i legit have no idea how i got it running on my NAS, but i had to shut it down cause the NAS ended up not being able to complete it in a days time :P NAS's are slow lol), then you can get the program to run automatically.

You can look at the code for the details. I'm pretty sure it just compiles the files into one video object, writes that object into the `db/outputs/` folder, then uploads it. I also know that it stores data such as what files it used and meta-data for each video, which you can find in the `states/` folder. Oh wait, I just removed `states/` from the git history because it had secrets there. Oh well. It will also make sure not to reuse files that were recently used.


### Notes

This project went through a few ideas before becoming whatever it is now. Originally, I was going to use clips from the Lego Movie, add captions, add audio, and upload them. Very simple. Then I had to figure out where the clips would come from, how to edit them, and how to get Google OAuth working. Less simple.

Some other ideas were anime clips (apparently there might be monetization issues), meme compilations (competitive), and Lego timelapses of scenes from movies, somehow involving AI. I ended up going with memes + a face + a background + music. You can probably tell which part of this project I actually figured out.

The original plan was to automatically download content into a `raw_memes` folder, edit it, and put the results into a `final_outputs` folder. Those were the original names, btw. See `db/outputs/` above for where the finished videos actually go. In the end, the plan became manually downloading memes, then having the program choose the files and do the editing. So yes, there is still some manual work. Unfortunately, memes do not just appear on my computer.

For the actual edits, I considered adding a face with an eyepatch, replacing black backgrounds with a blurred overlay, and shrinking the meme to make room for everything else. I settled on the face + background + music approach. The faces include my dawgs whose pictures I got from Immich. Removing the backgrounds was its own task. Of course.

At one point, I had 2 decent videos and wanted to get to 12. Uploading every 6 hours would give me (12 x 6 hours = 72 hours =) 3 days to make more. The eventual idea was to upload every 4 hours, skip the night, and vary the timing by +/- 15 minutes. These were plans, though, so don't assume that running the program will magically set up that exact schedule.

Other things on the list were preventing duplicate uploads and evening out file usage. My old notes say to change the data objects in `data.json`. The program does avoid recently used files, as mentioned above, but avoiding a recently used meme and avoiding uploading the exact same video are slightly different things.

Anyway, the development plan was basically:
1. Get the editing working
2. Acquire memes, music, faces, and backgrounds
3. Make the uploading script
4. Figure out how to keep it running
5. Debug
6. Debug
9. Debug
10. Wait

I did get it running on my Synology NAS using Docker, but, as mentioned earlier, the NAS was too slow. So the automation part also depends on having a computer that can actually finish making the videos. Small detail.


### Sources

For memes, I used Reddit, specifically r/dankmemes. My original notes somehow had a link to classical music under the memes section. Very helpful.

For music:
1. [Classical music on Pixabay](https://pixabay.com/music/search/classical/)
2. An Arabesque recording

I also wanted to get *Laputa* (*The Girl Who Fell from the Sky*) and all 3 movements of *First Suite*. Those were still on the acquire-later list, along with adding `.m4a` support. For now, the music files described above are `.mp3` files.

For backgrounds, I used [sunset videos from Videezy](https://www.videezy.com/free-video/sunset). I also had to think about compressing them, because apparently making a video out of other videos requires a lot of video.

For faces:
1. A cat picture. No clue where I got it.
2. Immich => ma DAWGS

These are the sources I used, btw, not a promise that everything on them is free to use or monetize. Check the permissions for whatever files you choose.


### Running Docker

The command I saved was:

```bash
docker compose run --rm cron
```

On my Synology, that looked like:

```bash
cd /volume1/docker/youtuber
docker compose run --rm cron
```

That path was where I put the project on my NAS. You should use wherever you put yours. Also, `cron` is the service name used in this command; just running this command isn't the same thing as setting up a recurring scheduled task.

The idea was to use scheduled tasks to run the container, make videos, and upload them. I do not remember enough of the setup to give you a trustworthy step-by-step guide, but the `dockerfile` and `compose.yaml` are there. Hopefully those, the command above, and some patience will get you somewhere.

Also, keep your uploading credentials and any state files containing secrets out of git. I already had to remove `states/` from the history once. Would prefer not to do that again lol.
