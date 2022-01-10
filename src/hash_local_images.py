"""
Get hash values for images in local albums
"""

from pathlib import Path
from PIL import Image
import imagehash


def get_hash(f):
    return imagehash.average_hash(Image.open(f))


def main():

    # get all files of interet
    file_list = []
    # for sub_dir in ['candy', 'dessert', 'dessert_corrected']:
    for sub_dir in ["dessert_corrected"]:
        dir_path = Path(f"/path/to/local/album/photos/{sub_dir}")
        file_list += list(dir_path.glob("**/*.[Jj][Pp][Gg]"))

    # hash the files
    total_files = len(file_list)
    hash_dict = {}
    for i, fpath in enumerate(file_list):
        hash_dict[fpath] = get_hash(fpath)

        if not (i + 1) % 50:
            print(f"Processed so far: {i+1}/{total_files}")

    # save hashes
    out = "data/interim/hashes_local_photos.tsv"
    with open(out, "w") as out_handle:
        for k, v in hash_dict.items():
            out_handle.write(f"{k}\t{v}\n")

    return None


if __name__ == "__main__":
    main()

