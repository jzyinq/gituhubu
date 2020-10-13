import concurrent.futures
import json
import re

import requests

from gituhubu.local_storage import ConfigFile


class GithubConfig:
    def __init__(self, organization, token):
        self.organization = organization
        self.token = token

    @staticmethod
    def from_file():
        config_file = ConfigFile()
        config = config_file.read()
        try:
            return GithubConfig(config['organization'], config['token'])
        except KeyError:
            raise RuntimeError(f"""Missing configuration in config.json.
Please create file '{config_file.file_path}' with following content:
```
{{
  "organization": "ORGANIZATION_NAME",
  "token": "API_TOKEN"
}}
```
ORGANIZATION_NAME is organization you want to search 
API_TOKEN is a github personal access token with minimum scope of `repos`.
More details here: 
https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token
""")


def _verify_response(response):
    if response.status_code != 200:
        raise RuntimeError(f"GitHub returned HTTP {response.status_code} with message:\n{response.content}")
    return response


class GitHubApi:
    def __init__(self, organization, api_token):
        self.ORGANIZATION = organization
        self.API_URL = "https://api.github.com"
        self.LIST_REPOS_URL = f"{self.API_URL}/orgs/{self.ORGANIZATION}/repos?sort=created&direction=desc"
        self.client = requests.Session()
        self.client.headers.update({
            'Authorization': 'token ' + api_token,
            'Accept': 'application/vnd.github.v3+json'
        })

    @staticmethod
    def extract_links_from_header(link_header):
        links = [l.strip() for l in link_header.split(',')]
        rels = {}
        pattern = r'<(?P<url>.*)>;\s*rel="(?P<rel>.*)"'
        for link in links:
            group_dict = re.match(pattern, link).groupdict()
            rels[group_dict['rel']] = group_dict['url']
        return rels

    def get_pages(self, link):
        response = _verify_response(self.client.get(link))
        links = self.extract_links_from_header(response.headers['link'])

        last_page = re.search(r'page=([0-9]+)', links['last'])
        pages = range(1, int(last_page[1]) + 1)
        link_without_page = links['last'].replace(last_page[0], '')
        links = []
        for i in pages:
            links.append(link_without_page + 'page=' + str(i))

        return links

    def get_organization_repos(self, link):
        organization_repos = {}
        response = _verify_response(self.client.get(link))
        json_response = json.loads(response.content)

        """ get names and ssh_url for clone """
        for json_object in json_response:
            organization_repos[json_object['name']] = {
                'ssh_url': json_object['ssh_url'],
                'full_name': json_object['full_name'],
            }

        return organization_repos

    def get_all_organization_repos(self):
        repo_pages = self.get_pages(self.LIST_REPOS_URL)
        organization_repos = {}
        worker_count = min(10, -(len(repo_pages) // -2))  # int division, avoid extra thread pass when page count raises
        with concurrent.futures.ThreadPoolExecutor(max_workers=worker_count) as executor:
            repo_dicts = executor.map(self.get_organization_repos, repo_pages)

        for repos in repo_dicts:
            organization_repos.update(repos)

        return organization_repos

    def get_repo_details(self, repository_name):
        response = _verify_response(self.client.get(f"{self.API_URL}/repos/{self.ORGANIZATION}/{repository_name}"))
        json_response = json.loads(response.content)
        return {
            'url': json_response['url'],
            'updated_at': json_response['updated_at'],
        }
