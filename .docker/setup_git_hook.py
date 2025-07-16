import subprocess
import os
import stat
import sys

def is_git_installed():
    """Check if Git is installed by running 'git --version'."""
    try:
        subprocess.run(["git", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def get_git_root():
    """Get the absolute path of the Git repository's root directory."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return os.path.abspath(result.stdout.strip())
    except subprocess.CalledProcessError:
        print("Error: Not inside a Git repository.")
        sys.exit(1)

def get_git_dir():
    """Get the absolute path of the .git directory."""
    return os.path.join(get_git_root(), ".git")

def get_docker_dir():
    """Get the absolute path of the .docker directory using WORKSPACE_DIR."""
    workspace_dir = os.environ.get("WORKSPACE_DIR")
    if not workspace_dir:
        print("Error: WORKSPACE_DIR environment variable is not set.")
        sys.exit(1)
    return os.path.abspath(os.path.join(workspace_dir, ".docker"))

def is_docker_in_git_repo(git_root, docker_dir):
    """Check if the .docker directory is within the Git repository."""
    return os.path.normpath(docker_dir).startswith(os.path.normpath(git_root))

def get_relative_docker_path(git_root, docker_dir):
    """Get the path of .docker relative to the Git repository root."""
    if not is_docker_in_git_repo(git_root, docker_dir):
        print(f"Error: .docker directory ({docker_dir}) is not within the Git repository ({git_root}).")
        sys.exit(1)
    return os.path.relpath(docker_dir, git_root)

def check_pre_commit_hook(hook_path):
    """Check if the pre-commit hook exists."""
    return os.path.isfile(hook_path)

def create_pre_commit_hook(hook_path, relative_docker_path):
    """Create a pre-commit hook with the chmod command for Linux only."""
    hook_content = f"""#!/bin/bash

# Get the Git repository root
GIT_ROOT=$(git rev-parse --show-toplevel)
DOCKER_DIR="$GIT_ROOT/{relative_docker_path}"

# Check if the system is Linux and not WSL
if [[ "$OSTYPE" == "linux-gnu"* && ! -d "/mnt/c" ]]; then
    # Check if .docker directory exists
    if [ -d "$DOCKER_DIR" ]; then
        sudo chmod 777 "$DOCKER_DIR"
        if [ $? -eq 0 ]; then
            echo "Permissions updated for .docker directory"
        else
            echo "Failed to update permissions for .docker directory"
            exit 1
        fi
    else
        echo "Error: .docker directory does not exist at $DOCKER_DIR"
        exit 1
    fi
else
    echo "Not running chmod on non-Linux system (e.g., Windows or WSL)"
fi

exit 0
"""
    try:
        with open(hook_path, "w") as f:
            f.write(hook_content)
        # Make the hook executable
        os.chmod(hook_path, os.stat(hook_path).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        print(f"Created pre-commit hook at {hook_path}")
    except OSError as e:
        print(f"Error: Failed to create pre-commit hook: {e}")
        sys.exit(1)

def main():
    # Check if Git is installed
    if not is_git_installed():
        print("Error: Git is not installed. Please install Git and try again.")
        sys.exit(1)

    # Get paths
    git_root = get_git_root()
    git_dir = get_git_dir()
    docker_dir = get_docker_dir()

    # Get the relative path of .docker
    relative_docker_path = get_relative_docker_path(git_root, docker_dir)

    # Check for pre-commit hook
    hook_path = os.path.join(git_dir, "hooks", "pre-commit")
    if check_pre_commit_hook(hook_path):
        print(f"Pre-commit hook already exists at {hook_path}")
    else:
        # Create the pre-commit hook
        create_pre_commit_hook(hook_path, relative_docker_path)

if __name__ == "__main__":
    main()