# plist
curses based interactive playlist creation for video files.

# usage

```
plist.exe --playlist c:\tmp\test.m3u --working-directory Z:\movies
```

# docs

Interactively create a `playlist.m3u` then launch it using `vlc.exe`. 
Automatically loads last playlist on startup.
There are 2 modes which you can toggle using the `ESC` key:
```
[INPUT: ENTER - add | ESC - CMD] 
[CMD: m - mod | q | w | p - play | r - reset]
```

In `INPUT` Mode, filenames in the playlist are searched for substrings that you enter, separated by a single whitespace. 

E.g.: `rick` `morty` `s01e01` would yield all filenames that contain all 3 strings.

In `CMD` mode you have the following options:

* `m` move
  * `j` navigate/move down
  * `k` navigate/move up
  * `d` del 
  * `m` toggle navigate/move
* `p` play: start vlc player with playlist
* `r` reset: reset the playlist
* `q` quit: doing nothing

# repo

https://github.com/dosnpfand/curses-playlist
