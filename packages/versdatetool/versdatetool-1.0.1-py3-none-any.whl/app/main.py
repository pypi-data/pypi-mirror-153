import os

import config
from app.models.Repository import *
from app.utils import utils, remote
from app.utils.Csv import *


def get_username_from_url(git_url):
    urllist = git_url.split("/")
    if len(urllist) < 5:
        # TODO: throw wrong url entered in csv
        pass

    return urllist[3]


def update_contents_locally(repo, clone_url, arg_obj):
    # To set parent directory as the head
    # TODO: Comment this
    # os.chdir("..")

    # Path where the cloned repo exists
    dir_path = remote.clone_repo(repo, clone_url)

    # Path where the "package.json" exists
    filepath = os.path.join(dir_path, config.FILENAME)

    utils.update_json(filepath, repo.dependency_name, arg_obj.dependency_version)

    remote.git_write_operations(dir_path, repo.dependency_name, repo.dependency_version, arg_obj.dependency_version)

    # Sending push request to the repo
    self_username = get_username_from_url(clone_url)
    pr_url = remote.generate_pr(repo.username, repo.reponame, self_username, repo.dependency_name,
                                repo.dependency_version, arg_obj.dependency_version)

    string_list = [repo.name, repo.url, repo.dependency_version, "false", pr_url]

    # writing to the csv
    Csv(arg_obj.output_path).append_row(string_list)
    return True


def update_contents(repo, arg_obj):
    """
    Update the content of the repository by making a fork of it & then makes a PR.
    :param repo:
    :return:
    """
    clone_url = remote.fork_repo(repo.username, repo.reponame)
    update_contents_locally(repo, clone_url, arg_obj)


def scrape_dependency(repo, arg_obj):
    # Extracting contents of config.FILENAME (package.json) from github repo
    contents = remote.extract_github_file(repo.username, repo.reponame, config.FILENAME)

    # Checking all the dependencies in config.FILENAME (package.json)
    for each in contents["dependencies"]:

        if each == arg_obj.dependency_name:
            repo.dependency_name = each
            repo.dependency_version = contents["dependencies"][each]

            # Checking if dependencies version doesn't exists
            if repo.dependency_version is None or repo.dependency_version == "":
                # TODO: Error invalid dependency version in the repository
                return False

            # For same dependency name, comparing versions
            if not utils.version_upto_date(repo.dependency_version, arg_obj.dependency_version):
                # Case 1: Version is not up to date
                # Checking if PR needs to be generated

                pr_link = ""
                if arg_obj.is_generate_pr:
                    update_contents(repo, arg_obj)

                    # pr_link = remote.generate_pr(repo.username, repo.reponame,
                    #                              repo.dependency_name,
                    #                              repo.dependency_version,
                    #                              arg_obj.dependency_version)
                else:
                    string_list = [repo.name, repo.url, repo.dependency_version, "false"]

                    # writing to the csv
                    Csv(arg_obj.output_path).append_row(string_list)
                    return True


            else:
                # Case 2: Version is up to date
                string_list = [repo.name, repo.url, repo.dependency_version, "true"]
                # writing to the csv
                Csv(arg_obj.output_path).append_row(string_list)
                return True

    # Case: When mentioned dependency name not found in the repository's config.FILENAME (package.json)
    string_list = [repo.name, repo.url, "N/A"]

    # writing to the csv
    Csv(arg_obj.output_path).append_row(string_list)

    # TODO: Error msg of mentioned dependency name not found in the repository's config.FILENAME (package.json)
    return False


def main():
    try:
        arg_obj = utils.parse_arg()

        all_repos = Csv(arg_obj.input_path).read_all()

        length = len(all_repos)

        if length > 1:
            # Adding header to the output csv file
            if arg_obj.is_generate_pr:
                Csv(arg_obj.output_path).write_row(config.output_header_with_pr)
            else:
                Csv(arg_obj.output_path).write_row(config.output_header)

        for i in range(1, length):
            current = all_repos[i]
            if len(current) < 2:
                # TODO: ERROR MSG for text not there in csv, skipping row
                continue
            my_repo = Repository(current[0], current[1])

            res = scrape_dependency(my_repo, arg_obj)
    except Exception as e:
        print(e)
