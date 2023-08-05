import logging
import os.path

from notetool.secret import read_secret

from github import Github


def all_file_to_github(git_path, repo_str=None, repo=None, access_tokens=None, recursive=False):
    if repo is None:
        access_tokens = access_tokens or read_secret(cate1='github', cate2='access_tokens', cate3='pygithub')
        g = Github(access_tokens)
        repo = g.get_repo(repo_str)

    all_files = []
    try:
        contents = repo.get_contents(git_path)
    except Exception as e:
        contents = repo.get_contents("")
        logging.warning(f"{git_path} not exists:{e}")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            if recursive:
                contents.extend(repo.get_contents(file_content.path))
        else:
            all_files.append(file_content.path)
    return all_files


def upload_data_to_github(content, git_path, repo_str):
    access_tokens = read_secret(cate1='github', cate2='access_tokens', cate3='pygithub')
    g = Github(access_tokens)
    repo = g.get_repo(repo_str)
    all_files = all_file_to_github(os.path.dirname(git_path), repo=repo)

    if git_path in all_files:
        contents = repo.get_contents(git_path)
        repo.update_file(contents.path, "committing files", content, contents.sha, branch="master")
        logging.info(f'{git_path} UPDATED')
    else:
        repo.create_file(git_path, "committing files", content, branch="master")
        logging.info(f'{git_path} CREATED')


def upload_file_to_github(file_path, *args, **kwargs):
    with open(file_path, 'r') as file:
        content = file.read()
        upload_data_to_github(content=content, *args, **kwargs)
