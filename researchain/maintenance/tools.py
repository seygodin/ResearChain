import git_manager
from pdb import set_trace

def git_handle(func_name, *args, **kwargs):
    set_trace()
    if not hasattr(git_manager, func_name):
        raise KeyError("git_manger library does not support the functions.")
    else:
        git_func_handle = getattr(git_manager, func_name)

        git_func_handle(*args, **kwargs)

def main():
    print("This tool controls github at high level")

if __name__ == "__main__":
    main()