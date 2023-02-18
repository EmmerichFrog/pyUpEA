# pyUpEA
Python script to autoupdate Yuzu EA (Pineapple builds).

Written with the Steam Deck gamemode and Emudeck in mind (but not limited to it), to allow for easy and/or automatic updates.

# Setup
1 - install the requirements with pip: `pip install -r requirements.txt`.
2 - run it: `python pyUpEA.py`. It accepts a path as an argument, if none is given uses the current working directory as destination.
(optional) - Can be built as a standalone binary with the included setup script, run it as `python setup.py build`. Requires cx_Freeze.

# How it works

It will download the lastest Yuzu EA AppImage in the selected directory and symlink it to `yuzu.AppImage` so that you can easily add it to Steam.
With subsequent runs it will check for new versions, backup the old version and update the symlink.

Can be used to also automatically check for updates whenever Yuzu is launched via gamemode by setting it as a launch option in Steam: as an example, if you built it as a binary `/path/to/pyUpEA /downloadPath && %command%`. For now, no feedback is given when ran like this. 
