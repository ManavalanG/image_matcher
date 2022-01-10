"""
Get hash values for thumbnail images 
"""

from pathlib import Path
from PIL import Image
import imagehash


def get_hash(f):
    return imagehash.average_hash(Image.open(f)) 


def main(indir, hashfile):

    hash_dict = {}
    for album_subdir in ([x for x in Path(indir).glob("*") if x.is_dir()]):
        image_files = list(album_subdir.glob("Image*"))
        for image in image_files:
            hash_dict[str(image)] = get_hash(image)

    with open(hashfile, 'w') as out_handle:
        for k, v in hash_dict.items():
            out_handle.write(f"{k}\t{v}\n")
        
    print (f"unique hash values: {len(set(hash_dict.values()))}")

    return None


if __name__=="__main__":
    for ALBUM_NUM in ['album_1', 'album_2', 'album_3']:
        print (f"Working on '{ALBUM_NUM}'")
        ALBUM_DIR = f"data/external/web_cache_thumbnails/{ALBUM_NUM}"
        HASH_OUTFILE = f"data/interim/webservice/{ALBUM_NUM}.tsv"
        main(ALBUM_DIR, HASH_OUTFILE)

