import os
import subprocess
from datetime import datetime
from typing import List

class GitHandler:
    def __init__(self):
        self.api_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'api')
        self.repo_dir = os.path.dirname(os.path.dirname(__file__))

    def has_changes(self) -> bool:
        """
        Checks if there are any changes in the api directory
        """
        try:
            # Get git status for api directory
            result = self._run_command(['git', 'status', '--porcelain', self.api_dir])
            return bool(result.strip())
        except subprocess.CalledProcessError as e:
            print(f"Error checking git status: {str(e)}")
            return False

    def commit_and_push(self):
        """
        Commits and pushes changes to the repository
        """
        try:
            # Stage changes in api directory
            self._run_command(['git', 'add', self.api_dir])

            # Create commit message
            commit_msg = f"Update political data: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}"
            self._run_command(['git', 'commit', '-m', commit_msg])

            # Push changes
            self._run_command(['git', 'push', 'origin', 'main'])
            
            print("Successfully pushed changes to repository")
        except subprocess.CalledProcessError as e:
            print(f"Error during git operations: {str(e)}")
            raise

    def _run_command(self, command: List[str]) -> str:
        """
        Runs a git command and returns its output
        """
        try:
            result = subprocess.run(
                command,
                cwd=self.repo_dir,
                check=True,
                capture_output=True,
                text=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Command failed: {' '.join(command)}")
            print(f"Error output: {e.stderr}")
            raise
