import platform
import subprocess

import iterfzf

from gituhubu.api import GitHubApi, GithubConfig
from gituhubu.local_storage import ReposCacheFile


def get_fuzzy_search(repository_names):
    return iterfzf.iterfzf(repository_names, exact=True, case_sensitive=False)


def clone_repository(ssh_url):
    return subprocess.run(["git", "clone", ssh_url])


def open_github(url_path):
    url = f"https://github.com/{url_path}"
    open_command = 'xdg-open'
    if platform.system() == "Darwin":
        open_command = 'open'

    # seems xdg-open stdout is messing with rofi at first launch when browser is not opened yet
    return subprocess.run([open_command, url], stdout=subprocess.DEVNULL)


def get_repositories(force_reload=False):
    repo_file = ReposCacheFile()
    repos = repo_file.read()
    config = GithubConfig.from_file()

    api = GitHubApi(config.organization, config.token)
    if force_reload:
        print('Updating local repository cache...')
        repos = api.get_all_organization_repos()
        repo_file.write(repos)
    if not repos:
        print('No local cache present.')
        print('Updating local repository cache...')
        repos = api.get_all_organization_repos()
        repo_file.write(repos)

    return repos
