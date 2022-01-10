# Identify matching photos from album using low-quality pictures as reference

## Task

Given a large photo album and thumbnails of a small subset of them, identify which photos in that album belong to those thumbnails.


## Background

- I used a webservice to choose select photos from a massive album for further downstream purposes, but in the end it turned out that this webservice couldn't properly handle handing off this selected photos info to the downstream vendor.
- Selected photos were in 100s (split in three parts) and album had several 1000s of pictures. So lot of work went into picking them.
- I had the complete photo album in my local computer.
- Unfortunately, this webservice didn't provide a way to export the selected photos in any form. Not even as filenames. Filenames they used in their website didn't match those in my local album anyway.
- After exploring all available options, it became clear that I had to use selected images from the webservice as reference and then redo the selection from the local photo album. 
- I could do it manually but that would be a mind-numbing and tedious job. And rather error prone.
- Fortunately after a bit of digging around, I was able to find a way to download thumbnail images of the selected images from the webservice. They were of poor quality but good enough to use as reference.
- These thumbnails opened up a possibility of programmatically identifying photos matching the thumbnails. 
- Having never done image processing(?) of this scale, this was an exciting task. Well, anything over having to manually doing it!


## How to?

Conda environment defined in [Config file](env.yaml) was used. PS: Surprised I didn't specify version of python and other dependencies in this conda environment. I think python version used was 3.7.x.

Scripts were ran in the order below. Header of the script has some description.

1. `src/pool_thumbnails.py`
2. `src/hash_local_images.py`
3. `src/fetch_matching_images.py`
4. `src/cleanup_selected_files.py`


## Notes

- This readme doc was written up after an year of actually completing the task. I rediscovered these scripts recently and figured I might as well share them here :)
- Scripts were written just enough to be functional. So try not to judge :)
