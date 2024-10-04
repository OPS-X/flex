import os
import time
from git import Repo, GitCommandError

# Define the path to your local repository
repo_path = r"D:\opsx_launch\flex"  # Use raw string notation for Windows paths

# Open the repository
try:
    repo = Repo(repo_path)
    assert not repo.bare
except GitCommandError as e:
    print(f"Error: {e}")
    exit(1)

# Loop to continuously check for changes and sync
while True:
    try:
        # Pull latest changes from remote
        print("Pulling latest changes from remote...")
        repo.remotes.origin.pull()

        # Check for uncommitted changes
        if repo.is_dirty(untracked_files=True):
            print("Detected changes, committing and pushing...")
            
            # Add all changes
            repo.git.add(A=True)

            # Commit with a timestamp message
            repo.index.commit(f"Auto-sync: {time.ctime()}")

            # Push to the remote repository
            repo.remotes.origin.push()
            print("Changes pushed successfully.")
        else:
            print("No changes to sync.")
    except GitCommandError as e:
        print(f"Git command error: {e}")

    # Wait for a specified interval (e.g., 30 seconds) before the next sync
    print("Waiting for the next cycle...")
    time.sleep(30)
