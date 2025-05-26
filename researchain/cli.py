# researchain/cli.py
from pdb import set_trace
import sys
import argparse
import subprocess
from . import git_manager

def main():
    parser = argparse.ArgumentParser(prog="researchain",
                                     description="Research-AI 패키지 커맨드라인 인터페이스")
    subparsers = parser.add_subparsers(dest="command", required=True)
    git_parser = subparsers.add_parser("git",help="git_manager.github 모듈 실행")
    git_parser.add_argument("--git_func", default=None, choices=[None, 'init_repo', "update_repo", "change_branch", "auto_set"])
    git_parser.add_argument("--comment", type=str)
    args = parser.parse_args()

    print(args)

    # TODO: 실제 로직을 여기에 구현
    set_trace()
    if args.command == "git":
        if hasattr(git_manager.github, args.git_func):
            git_handle = getattr(git_manager.github, args.git_func)
            git_handle() if args.comment is None else git_handle(args.comment)
        else:
            raise ValueError(f"The function ({args.git_func}) does not included in git_manager.")

if __name__ == "__main__":
    main()
