import os
import time
from git import Repo, GitCommandError

# Define the path to your local repository
repo_path = r"D:\opsx_launch\flex"  # Use raw string notation for Windows paths or set it to your project path

# Files or directories to exclude from the commit
exclude_files = ['auto-sync.sh', '.gitignore', 'README.md']  # Add files or directories you want to exclude

# Set up logging level (can add a logging library for advanced logging if needed)
def log(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"[{timestamp}] {message}")

# Function to check for changes in specific file types (e.g., *.html)
def check_for_changes(repo, file_extensions=None):
    """
    Check if there are any changes in the repository for specific file extensions.
    :param repo: Git repository object
    :param file_extensions: List of file extensions to track (e.g., ['html', 'css'])
    :return: List of changed files
    """
    changed_files = [item.a_path for item in repo.index.diff(None) if not any(item.a_path.endswith(ext) for ext in exclude_files)]

    # Filter by specific file extensions if provided
    if file_extensions:
        changed_files = [file for file in changed_files if any(file.endswith(ext) for ext in file_extensions)]

    return changed_files

# Open the repository
try:
    repo = Repo(repo_path)
    assert not repo.bare
    log("Repository loaded successfully.")
except GitCommandError as e:
    log(f"Error: {e}")
    exit(1)

# Loop to continuously check for changes and sync
while True:
    try:
        # Pull latest changes from remote (if needed, but not required for local-only sync)
        log("Checking for any incoming changes from the remote repository...")
        repo.remotes.origin.pull()  # Optional: remove or comment if not needed

        # Check for changes in specific file types (e.g., HTML files)
        modified_files = check_for_changes(repo, file_extensions=['html'])

        if modified_files:
            log(f"Detected changes in files: {', '.join(modified_files)}")

            # Add only the changed files, excluding those in the exclude list
            for file in modified_files:
                if file not in exclude_files:
                    repo.git.add(file)
                    log(f"Added file: {file}")

            # Commit changes with a detailed message
            commit_message = f"Auto-sync: {time.ctime()}\n\nFiles changed:\n" + "\n".join(modified_files)
            repo.index.commit(commit_message)
            log("Committed changes locally.")

            # Push changes to the remote repository
            repo.remotes.origin.push()
            log("Changes pushed to the remote repository successfully.")
        else:
            log("No changes to sync.")

    except GitCommandError as e:
        log(f"Git command error: {e}")

    # Wait for a specified interval (e.g., 30 seconds) before the next sync
    log("Waiting for the next cycle...")
    time.sleep(30)
