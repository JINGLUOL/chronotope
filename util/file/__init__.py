import os
import re


def copy_a_folders_filename(folder_path, regex='[.]*'):
    if os.path.exists(folder_path):
        files = []
        for file in os.listdir(folder_path):
            re_file = re.search(regex, file)
            files.append(re_file and re_file.group() or file)
        return '\n'.join(files)
    return ''


def files_name_only_matching(folder_path, match_names: list[str]) -> list[str | None]:
    result: list[str | None] = [None for _ in range(len(match_names))]
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            file_name = '.' in file and file.split('.')[0] or file
            if file_name in match_names:
                result[match_names.index(file_name)] = file_path
    return result
