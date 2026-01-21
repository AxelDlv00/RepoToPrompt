import os
import json
from rich.progress import track

class RepoProcessor:
    def __init__(self, repo_path, ignore_manager, options=None):
        self.repo_path = repo_path
        self.im = ignore_manager
        self.options = options or {}
        self.stats = {"processed": 0, "ignored": 0}

    def is_binary(self, file_path):
        """Detects binary files by checking for null bytes."""
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(1024)
            return b'\0' in chunk
        except:
            return True

    def clean_notebook(self, content):
        """Removes output cells from .ipynb files to minimize token usage."""
        try:
            data = json.loads(content)
            if "cells" in data:
                for cell in data["cells"]:
                    if "outputs" in cell:
                        cell["outputs"] = []
                    if "execution_count" in cell:
                        cell["execution_count"] = None
            return json.dumps(data, indent=1)
        except:
            return content

    def process(self, output_file):
        """Walks the directory and writes filtered content."""
        all_files = []
        for root, _, files in os.walk(self.repo_path):
            for name in files:
                all_files.append(os.path.join(root, name))

        for full_path in track(all_files, description="[cyan]Processing repository..."):
            rel_path = os.path.relpath(full_path, self.repo_path)

            if self.im.should_ignore(rel_path):
                self.stats["ignored"] += 1
                continue

            if self.options.get('skip_binary', True) and self.is_binary(full_path):
                self.stats["ignored"] += 1
                continue

            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                if rel_path.endswith(".ipynb"):
                    content = self.clean_notebook(content)

                output_file.write(f"----\n{rel_path}\n{content}\n")
                self.stats["processed"] += 1
            except Exception:
                self.stats["ignored"] += 1