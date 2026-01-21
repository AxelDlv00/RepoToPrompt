import os
import fnmatch

# Comprehensive default ignore patterns
DEFAULT_IGNORE = """
# Folders
.git/
__pycache__/
node_modules/
venv/
.venv/
build/
dist/
.idea/
.vscode/

# Binaries & Media
*.log
*.png
*.jpg
*.jpeg
*.gif
*.svg
*.pdf
*.exe
*.bin
*.pyc
*.DS_Store
*.zip
*.tar.gz
*.mp4

# Project specific
output.txt
.RepoToPromptignore
"""

class IgnoreManager:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.ignore_patterns = []

    def create_default_ignore(self, force=False):
        """Creates a default ignore file. Overwrites if force is True."""
        ignore_path = os.path.join(self.repo_path, ".RepoToPromptignore")
        if not os.path.exists(ignore_path) or force:
            with open(ignore_path, "w", encoding="utf-8") as f:
                f.write(DEFAULT_IGNORE.strip())
            return True
        return False

    def load_patterns(self):
        """Loads patterns from .RepoToPromptignore."""
        ignore_path = os.path.join(self.repo_path, ".RepoToPromptignore")
        if os.path.exists(ignore_path):
            with open(ignore_path, "r") as f:
                self.ignore_patterns = [
                    line.strip() for line in f 
                    if line.strip() and not line.startswith("#")
                ]

    def should_ignore(self, relative_path):
        """Matches path against ignore patterns."""
        parts = relative_path.split(os.sep)
        for i in range(1, len(parts) + 1):
            sub_path = os.sep.join(parts[:i])
            for pattern in self.ignore_patterns:
                if fnmatch.fnmatch(sub_path, pattern) or fnmatch.fnmatch(parts[i-1], pattern):
                    return True
        return False