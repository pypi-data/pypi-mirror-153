import argparse
import csv
import requests
import base64
import json
from prettytable import PrettyTable

global username, access_token, email

repos = dict()
github_api_url = "https://api.github.com/repos/"


def set_input(path_to_csv_file):
    try:
        file = open(path_to_csv_file)
    except:
        return False
    csvreader = csv.reader(file)
    next(csvreader)

    for row in csvreader:
        repos[row[0].strip()] = row[1].strip()

    file.close()
    return True


def output_to_csv(table):
    with open("./output.csv", "w") as fp:
        writer = csv.writer(fp, delimiter=",", lineterminator="\n")
        for row in table:
            writer.writerow([i for i in row])


def version_compare(v1, v2):

    a1 = v1.split(".")
    a2 = v2.split(".")
    n = len(a1)
    m = len(a2)

    a1 = [int(i) for i in a1]
    a2 = [int(i) for i in a2]

    if n > m:
        for i in range(m, n):
            a2.append(0)
    elif m > n:
        for i in range(n, m):
            a1.append(0)

    # returns 1 if version 1 is bigger and -1 if
    # version 2 is bigger and 0 if equal
    for i in range(len(a1)):
        if a1[i] > a2[i]:
            return 1
        elif a2[i] > a1[i]:
            return -1
    return 0


def get_api_url(repo_url):
    _, url = repo_url.split("https://github.com/")
    url = github_api_url + url
    if url[-1] != "/":
        url += "/"
    url += "contents/package.json"
    return url


def get_fork_url(repo_url):
    # print(repo_url)
    _, url = repo_url.split("https://github.com/")
    # print(url)
    parts = url.split("/")
    # print(parts)
    parts[0] = username
    url = "/".join(parts)
    url = github_api_url + url
    if url[-1] != "/":
        url += "/"
    url += "contents/package.json"
    return url


def fork_api_url(repo_url):
    _, url = repo_url.split("https://github.com/")
    url = github_api_url + url
    if url[-1] != "/":
        url += "/"
    url += "forks"
    return url


def pr_api_url(repo_url):
    _, url = repo_url.split("https://github.com/")
    url = github_api_url + url
    if url[-1] != "/":
        url += "/"
    url += "pulls"
    return url


def create_fork(repo_url):
    url = fork_api_url(repo_url)
    # print(url)
    rpost = requests.post(url, auth=(username, access_token))
    # print('create_fork',rpost.json())


def create_pr(repo_url, title, body, head, base):
    payload = {
        "title": title,
        "body": body,
        "head": head,
        "base": base,
    }
    payload = json.dumps(payload)
    # print(payload)
    url = pr_api_url(repo_url)
    # print('url',url)
    rpost = requests.post(url, auth=(username, access_token), data=payload)
    # print('create_pr',rpost)
    res = rpost.json()
    # print('create_pr',res)
    return res["html_url"]


def get_package_json(repo_url):
    url = get_api_url(repo_url)
    req = requests.get(url)
    if req.status_code == requests.codes.ok:
        req = req.json()
        content = base64.b64decode(req["content"])
        package_json = json.loads(content)
        return package_json, req["sha"]


def update_package_json(package_json, sha, repo_url, message):
    package_json = json.dumps(package_json, indent=3)
    package_json_bytes = package_json.encode("utf-8")
    package_json_base64 = str(base64.b64encode(package_json_bytes))
    # print('content',package_json_base64[2:-1])

    payload = {
        "message": message,
        "committer": {"name": username, "email": email},
        "content": package_json_base64[2:-1],
        "sha": sha,
    }

    payload = json.dumps(payload)
    # print('update_package_json',payload)
    url = get_fork_url(repo_url)
    # print('update_package_json',url)
    rput = requests.put(url, auth=(username, access_token), data=payload)
    # print('update_package_json',rput.json())


def check_versions(dependency, version):
    output = []
    for repo in repos:
        out_res = [repo, repos[repo], None, None]
        package_json, _ = get_package_json(repo_url=repos[repo])
        if package_json != None:
            actual_version = package_json["dependencies"][dependency]
            if actual_version[0] == "^":
                actual_version = actual_version[1:]
            out_res[2] = actual_version
            if (
                dependency in package_json["dependencies"]
                and version_compare(actual_version, version) >= 0
            ):
                out_res[3] = True
            else:
                out_res[3] = False
        output.append(out_res)
        # print(*out_res)
    return output


def update_versions(checked_output, dependency, version):
    output = []
    for repo, repo_url, actual_version, isupdated in checked_output:
        updated_info = [repo, repo_url, actual_version, isupdated, ""]
        # print('update_versions',repo,repo_url,isupdated)
        if not isupdated:
            create_fork(repo_url)
            package_json, sha = get_package_json(repo_url)
            if dependency in package_json["dependencies"]:
                package_json["dependencies"][dependency] = "^" + version
                msg = (
                    "update "
                    + dependency
                    + " version from "
                    + actual_version
                    + " to "
                    + version
                )
                update_package_json(package_json, sha, repo_url, msg)
            pr_url = create_pr(
                repo_url,
                str(dependency) + " version changed to " + str(version),
                "Updates the version of "
                + str(dependency)
                + " from "
                + str(actual_version)
                + " to "
                + str(version),
                username + ":main",
                "main",
            )
            updated_info[4] = pr_url
        output.append(updated_info)
        # print(*updated_info)
    return output


def display(table):
    t = PrettyTable(table[0])
    t.add_rows(table[1:])
    print(t)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-input", action="store", type=str, help="Enter input file name", required=True
    )
    parser.add_argument(
        "-update",
        action="store_true",
        help="use for updating the version and creating pr",
    )
    parser.add_argument(
        "dependency", metavar="dep", type=str, help="Enter dependency_name@version"
    )

    args = parser.parse_args()

    # print(args.input)
    # print(args.dependency)
    # print(args.update)
    taken = set_input(path_to_csv_file=args.input)
    if taken:
        # print(repos)
        if args.update:
            username = input("Enter github username:")
            email = input(
                "Enter email linked with github username (necessary for update and pr):"
            )
            access_token = input("Enter github access token:")

        dep, ver = args.dependency.split("@")
        # print(dep, ver)
        try:
            checked_output = check_versions(dependency=dep, version=ver)

            if args.update:
                updated_output = update_versions(
                    checked_output, dependency=dep, version=ver
                )
                updated_output.insert(
                    0, ["name", "repo", "version", "version_satisfied", "update_pr"]
                )
                display(updated_output)
                output_to_csv(updated_output)
            else:
                checked_output.insert(
                    0, ["name", "repo", "version", "version_satisfied"]
                )
                display(checked_output)
                output_to_csv(checked_output)
            print("output saved in output.csv !")
        except:
            print(
                "Github api limit exceeded. Please try after sometime or with a different ip address."
            )
    else:
        print("No file found!")

# if __name__ == "__main__":
#     main()