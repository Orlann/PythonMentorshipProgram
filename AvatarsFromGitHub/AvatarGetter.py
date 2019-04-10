import os
import argparse
import pathlib
import requests

USERNAME = ''
PASSWORD = ''


def main(git_user, git_project):
    # ------- Directory creation
    new_dir = f"{os.getcwd()}\\{git_user}\\{git_project}"
    pathlib.Path(new_dir).mkdir(parents=True, exist_ok=True)
    os.makedirs(new_dir, exist_ok=True)

    # ------ Get response from URL and put avatar-jpg in appropriate directory
    url = f"https://api.github.com/repos/{git_user}/{git_project}/contributors"
    r = requests.get(url, auth=(USERNAME, PASSWORD), stream=True)
    response_array = r.json()
    for item in response_array:
        key = item['login']
        value = item['avatar_url']
        file_name = f"{new_dir}/{key}.jpg"

        avatar_response = requests.get(value, stream=True)
        with open(file_name, 'wb') as avatar_file:
            avatar_file.write(avatar_response.content)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Input user and project for GitHub')
    parser.add_argument('-u', '--user', required=True, help="Input user name for GitHub")
    parser.add_argument('-p', '--project', required=True, help="Input project name for GitHub")
    args = parser.parse_args()
    main(args.user, args.project)

