"""
Using hash values of thumbnails and full resolution photos, identify identical and similar images
"""

from pathlib import Path
from PIL import Image
import imagehash
from shutil import copy2
import pprint


def get_hash_dict(f, skip_duplicates=False):

    d = {}
    with open(f) as f_handle:
        for line in f_handle:
            line = line.strip().split("\t")

            fpath = line[0]
            hash_val = line[1]

            if skip_duplicates:
                if hash_val not in d:
                    d[hash_val] = fpath
            else:
                if hash_val not in d:
                    d[hash_val] = []

                d[hash_val].append(fpath)

    return d


def get_diff_score(a, b):
    diff_score = imagehash.hex_to_hash(a) - imagehash.hex_to_hash(b)
    return diff_score


def correct_for_corrected(fpath_list):

    dessert = [Path(x).name.lower() for x in fpath_list if "/dessert/" in x]

    new_list = []
    for fpath in fpath_list:
        if "dessert_corrected" in fpath:
            if Path(fpath).name.lower() in dessert:
                continue
        new_list.append(fpath)

    return new_list


# def copy_files(source_file, dest_dir):

#     copy2(source_file, dest_dir)

#     return None


def write_query_files(query_dict, album):
    query_only_outdir = Path(f"data/processed/{album}/query_only")
    query_only_outdir.mkdir(exist_ok=True, parents=True)

    for i, (query_hash, query_file) in enumerate(query_dict.items()):
        copy2(query_file, query_only_outdir / f"{i+1}.jpeg")

    return None


def process_match_files(query_match_dict, album, match_type):

    query_match_outdir = Path(f"data/processed/{album}/{match_type}/query_and_targets")
    match_only_outdir = Path(f"data/processed/{album}/{match_type}/targets")
    # query_match_outdir.mkdir(exist_ok=True, parents=True)
    # (match_only_outdir / "single").mkdir(exist_ok=True, parents=True)
    # (match_only_outdir / "multiple").mkdir(exist_ok=True, parents=True)
    # (match_only_outdir / "no_match").mkdir(exist_ok=True, parents=True)
    for subdir_name in ["single", "multiple", "no_match"]:
        (match_only_outdir / subdir_name).mkdir(exist_ok=True, parents=True)
        (query_match_outdir / subdir_name).mkdir(exist_ok=True, parents=True)

    for i, (query, match_list) in enumerate(query_match_dict.items()):
        # query_outfile = outdir / "query_and_targets" / f"{i+1}.jpeg"

        # query_outfile = query_match_outdir / f"{i+1}.jpeg"
        # copy2(query, query_outfile)

        if match_list:
            count_type = "single" if len(match_list) == 1 else "multiple"
            for match in match_list:
                # both query and targets
                copy2(
                    match,
                    query_match_outdir / count_type / f"{i+1}_{Path(match).name}.jpeg",
                )
                copy2(query, query_match_outdir / count_type / f"{i+1}.jpeg")

                # target only
                copy2(
                    match,
                    match_only_outdir / count_type / f"{i+1}_{Path(match).name}.jpeg",
                )
        else:
            copy2(query, match_only_outdir / "no_match" / f"{i+1}.jpeg")

    return None


def main(album):

    # photoes selected in webservice
    webservice_hash_f = f"data/interim/webservice/{album}.tsv"
    webservice_hash_dict = get_hash_dict(webservice_hash_f, skip_duplicates=True)
    print(len(webservice_hash_dict))

    # local photos
    # targets_hash_f = "data/interim/hashes_local_photos-noCorrection.tsv"
    targets_hash_f = "data/interim/hashes_local_photos-combined.tsv"
    targets_hash_dict = get_hash_dict(targets_hash_f)
    # print (len(targets_hash_dict))

    identical_dict = {}
    similar_dict = {}
    for query_hash, query_file in webservice_hash_dict.items():
        ##### find identical images #####
        if query_hash in targets_hash_dict:
            matches = targets_hash_dict[query_hash]

            identical_dict[query_file] = correct_for_corrected(matches)
            # if len(identical_dict[query_file]) > 1:
            #     print (f"open '{webservice_hash_dict[query_hash]}' {' '.join(identical_dict[query_file])}")
            # for f in identical_dict[query_file]

        ##### find similar images #####
        else:
            similar_files_dict = {}
            for target_hash, target_file in targets_hash_dict.items():
                diff_score = get_diff_score(query_hash, target_hash)
                if diff_score < 5:
                    if diff_score not in similar_files_dict:
                        similar_files_dict[diff_score] = []
                    similar_files_dict[diff_score] += target_file

            # pprint.pprint(similar_files_dict)
            if 1 in similar_files_dict:
                similar_dict[query_file] = correct_for_corrected(similar_files_dict[1])
            elif 2 in similar_files_dict:
                similar_dict[query_file] = correct_for_corrected(similar_files_dict[2])
            elif 3 in similar_files_dict:
                similar_dict[query_file] = correct_for_corrected(similar_files_dict[3])
            elif 4 in similar_files_dict:
                similar_dict[query_file] = correct_for_corrected(similar_files_dict[4])

            if query_file not in similar_dict:
                similar_dict[query_file] = []

    write_query_files(webservice_hash_dict, album)
    process_match_files(identical_dict, album, match_type="identical")
    process_match_files(similar_dict, album, match_type="similar")

    return None


if __name__ == "__main__":
    for album in ["album_1", "album_2", "album_3"]:
        main(album)

