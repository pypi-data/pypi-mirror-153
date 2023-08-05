import argparse
from sys import platform
import os 
import subprocess
from sysflow.utils import load 
import re 

def parse_args():
    desc = "utils functions to better support Github"
    parser = argparse.ArgumentParser(description=desc)
    arg_lists = []

    def add_argument_group(name):
        arg = parser.add_argument_group(name)
        arg_lists.append(arg)
        return arg

    # github arg
    github_arg = add_argument_group("github")
    github_arg.add_argument("url", type=str, help="github url to clone")
    args = parser.parse_known_args()

    return args


def github_clone(url):
    if platform == "linux" or platform == "linux2":
        # linux
        bash_profile = load(os.path.join(os.environ['HOME'], '.bashrc'))
    elif platform == "darwin":
        # OS X
        bash_profile = load(os.path.join(os.environ['HOME'], '.bash_profile'))
    elif platform == "win32":
        assert False, "Windows is not supported"
        
    access_token = re.findall(r"alias gk=\"echo -e '(.*)' \| pbcopy\"", bash_profile)[0]

    username_cmd = 'git config user.name'
    username = subprocess.Popen(username_cmd.split(), stdout=subprocess.PIPE).communicate()[0].strip().decode('utf-8')

    url_template = "github.com[/:](.*)/(.*)"
    url_username, repo_name = re.findall(url_template, url)[0]
    repo_name = repo_name.replace(".git", "")

    if url_username == username: 
        cmd = "git clone https://{username}:{access_token}@github.com/{username}/{repo_name}.git".format(username=username, access_token=access_token, repo_name=repo_name)
    else: 
        cmd = "git clone {url}".format(url=url)
        
    subprocess.call(cmd, shell=True)


def main():
    global args
    args = parse_args()

    url = args[0].url
    github_clone(url)


if __name__ == "__main__":
    main()
