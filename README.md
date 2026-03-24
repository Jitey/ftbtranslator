# Description

Simple tool that help the translation of Star Techology modpack using Google Translation.  
It is not 100% accurate, you actually need to check out every translation to find translation error.

# Installation

Simply clone this repo and then install dependancy using
```
uv sync
```

# Usage

## Step 1

If you're curently working on Minecraft Translation Helper tool, you need to exporte the whole workspace. It will give you a single json file to place in ```workspaces/imported```.
Execute the tile ```mth.py```. You can replace the name of the file in the call of ```import_workspace()``` if your doesn't correspondent. This next script will rebuild in ```translation/new```  the ```kubejs/assets``` folder
If you're not working with MTH tool but directly on kubejs folder you can then put this folder in ```translations/old```.

## Step 2

The next step is the translation of all lg_lg.json files. To start it simply execute ```translator.py```. It will parse every sub folder of ```translations/old/kubejs/assets```, translate every row and then write it in a new lg_lg.json in ```translations/new/kubejs/assets```