#!/usr/bin/env python3
"""
GitHub Manage Tool

Provides the following commands for a project folder:

1. init       - Initialize a GitHub repository named after the project folder, commit all files (excluding images and model files), and push to GitHub.
2. update     - Create a new branch named with the date and custom comment, commit changes, and push it.
3. change     - Checkout a specified branch.
4. auto_set   - Generate requirements.txt from the current environment.

Usage examples:
  export GITHUB_TOKEN=<your_token>
  python github_manage_tool.py init
  python github_manage_tool.py update --date 20250508 --comment "bugfix"
  python github_manage_tool.py change feature-branch
  python github_manage_tool.py auto_set
"""
import os
import sys
import subprocess
import argparse
from datetime import datetime

# Attempt to import requests or exit
try:
    import requests
except ImportError:
    print("Error: requests library is required. Install with `pip install requests`.")
    sys.exit(1)

GITHUB_API_URL = "https://api.github.com"


def run(cmd, check=True):
    """Run a shell command and print its invocation."""
    print(f">>> {cmd}")
    subprocess.run(cmd, shell=True, check=check)


def get_repo_name():
    """Derive the repository name from the current folder name."""
    return os.path.basename(os.getcwd())


def init_repo():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise KeyError("GITHUB_TOKEN environment variable is not set. Please set the token using 'export GITHUB_TOKEN=<YOUR_TOKEN>'")

    repo_name = get_repo_name()

    # Generate .gitignore to exclude images and model checkpoints
    patterns = ["*.png", "*.jpg", "*.jpeg", "*.pt", "*.ckpt", "*.pth"]
    with open('.gitignore', 'w') as gi:
        gi.write("\n".join(patterns) + "\n")
    print(".gitignore created with patterns to exclude images and checkpoints.")

    # Create repository via GitHub API
    url = f"{GITHUB_API_URL}/user/repos"
    headers = {"Authorization": f"token {token}"}
    payload = {"name": repo_name, "private": False}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 201:
        print(f"Failed to create repo: {response.status_code} - {response.text}")
        sys.exit(1)

    owner = response.json()["owner"]["login"]
    # Use HTTPS remote URL with token for non-interactive authentication
    remote_url = f"https://{token}@github.com/{owner}/{repo_name}.git"

    # Initialize local git repository
    run("git init")
    run("git add .")
    run('git commit -m "Initial commit"')
    run("git branch -M main")
    run(f"git remote add origin {remote_url}")
    run("git push -u origin main")
    print(f"Repository '{repo_name}' initialized and pushed to GitHub.")


def update_repo(comment, date_str=None):
    comment = comment
    date_str = date_str if date_str is not None else datetime.now().strftime("%Y%m%d")

    branch = f"update-{date_str}-{comment.replace(' ', '-')[:50]}"

    run("git fetch origin")
    run(f"git checkout -b {branch}")
    run("git add .")
    run(f'git commit -m "{comment}"')
    run(f"git push origin {branch}")
    print(f"Changes committed to branch '{branch}'.")


def change_branch(branch):
    run("git fetch origin")
    run(f"git checkout {branch}")
    print(f"Switched to branch '{branch}'.")


def auto_set():
    # Generate requirements.txt using pip freeze
    run("pip freeze > requirements.txt")
    print("requirements.txt generated.")


def main():
    parser = argparse.ArgumentParser(description="GitHub Manage Tool for automating GitHub operations.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init", help="Initialize GitHub repository and push initial commit.")

    p_update = subparsers.add_parser("update", help="Create branch, commit changes, and push.")
    p_update.add_argument("--date", help="Date for branch name in YYYYMMDD format.")
    p_update.add_argument("--comment", required=True, help="Commit message and branch descriptor.")

    p_change = subparsers.add_parser("change", help="Checkout a specific branch.")
    p_change.add_argument("branch", help="Branch name to checkout.")

    subparsers.add_parser("auto_set", help="Auto-generate requirements.txt from current environment.")

    args = parser.parse_args()
    if args.command == "init":
        init_repo()
    elif args.command == "update":
        update_repo(comment=args.comment, date_str=args.date)
    elif args.command == "change":
        change_branch(args.branch)
    elif args.command == "auto_set":
        auto_set()

if __name__ == "__main__":
    main()