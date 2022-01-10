from pathlib import Path
from shutil import copy2


def filename_to_filepath_dict(dirpath, remove_underscore=False):

    d = {}
    for fpath in Path(dirpath).glob("**/*.[Jj][Pp][Gg]"):
        basename = fpath.name
        without_ext = basename.split(".")[0]
        if remove_underscore:
            without_ext = "_".join(without_ext.split("_")[1:])

        # print (without_ext)
        d[without_ext] = str(fpath)

    return d


def main():

    # get all files in local album
    all_files_dict = {}
    for sub_dir in ["candy", "dessert", "dessert_corrected"]:
        dir_path = Path(f"/path/to/local/album/photos/{sub_dir}")
        all_files_dict[sub_dir] = filename_to_filepath_dict(dir_path)
        # print (len(all_files_dict[sub_dir]))

    for album_no in ["album1", "album2", "album3"]:

        album_path = f"data/delete_chosen_for_albums/{album_no}"
        album_dict = filename_to_filepath_dict(album_path, remove_underscore=True)
        print(len(album_dict))

        main_targets = []
        dessert_only_targets = []
        for filename in album_dict:
            if filename in all_files_dict["candy"]:
                main_targets.append(all_files_dict["candy"][filename])
            elif filename in all_files_dict["dessert_corrected"]:
                main_targets.append(all_files_dict["dessert_corrected"][filename])
                dessert_only_targets.append(all_files_dict["dessert"][filename])
            elif filename in all_files_dict["dessert"]:
                main_targets.append(all_files_dict["dessert"][filename])
            else:
                print(f"oooops... '{filename}'",)
                raise SystemExit(1)

        # save main pics
        out_dir = Path(f"data/processed/almost_final/{album_no}/main")
        out_dir.mkdir(parents=True, exist_ok=True)
        for item in main_targets:
            copy2(item, out_dir)

        # save alternative pics just in case. These are brighness unadjusted "dessert" pics
        out_dir = Path(f"data/processed/almost_final/{album_no}/brightness_uncorrected")
        out_dir.mkdir(parents=True, exist_ok=True)
        for item in dessert_only_targets:
            copy2(item, out_dir)

        # break

    return None


if __name__ == "__main__":
    main()

