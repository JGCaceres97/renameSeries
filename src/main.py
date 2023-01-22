#!/usr/bin/python3

from pathlib import Path
from argparse import ArgumentParser
from os import path, scandir
from json import loads
from subprocess import getstatusoutput


def main():
    parser = ArgumentParser(description="Rename show's files on a folder")
    parser.add_argument(
        "-d", "--directory", required=True, help="directory containing show files to rename"
    )
    parser.add_argument("-s", "--season", required=True, help="season from the media")

    args = parser.parse_args()

    dir = Path(args.directory)
    if not dir.exists():
        print("The target directory does not exists")
        exit(1)

    seasonInt: int = int(args.season)
    if seasonInt < 1:
        print("season provided is not valid")
        exit(1)

    season: str
    episode: int = 0
    if seasonInt < 10:
        season = "0" + str(seasonInt)
    else:
        season = str(seasonInt)

    with scandir(dir) as files:
        for file in sorted(files, key=lambda e: e.name):
            if file.is_dir():
                continue

            if not file.name.endswith((".mkv", ".mp4", ".avi")):
                continue

            print(file.name + "...", end=" ")

            episode += 1
            episodeStr: str

            if episode < 10:
                episodeStr = "0" + str(episode)
            else:
                episodeStr = str(episode)

            success_rename = renameFile(file.path, file.name, season, episodeStr)

            if not success_rename:
                print("ERROR RENAMING")
                continue

            print("OK")


def normalize_path(pathStr: str) -> str:
    return path.normpath('"' + pathStr + '"')


def get_title_from_filename(file_name: str) -> str:
    return file_name.split(" - ")[1].split(".mkv")[0].strip()


def get_folder_from_path(pathStr: str) -> str:
    folders: list[str] = pathStr.split("/")
    folder_path: str = ""

    for i in range(len(folders)):
        if i == len(folders) - 1:
            continue

        folder_path += folders[i] + "/"

    return folder_path


def renameFile(pathStr: str, file_name: str, season: str, episode: str) -> bool:
    folder_path: str = get_folder_from_path(pathStr)
    title = get_title_from_filename(file_name)
    prefix: str = "S" + season + "E" + episode

    command = (
        "mv " + normalize_path(pathStr) + " " + normalize_path(folder_path + prefix + " - " + title)
    )

    result = getstatusoutput(command.strip())
    return result[0] == 0


main()
