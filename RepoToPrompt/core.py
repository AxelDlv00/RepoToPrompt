import os
import json
from rich.progress import track

class RepoProcessor:
    def __init__(self, repo_path, ignore_manager, display, options=None):
        self.repo_path = repo_path
        self.im = ignore_manager
        self.display = display  
        self.options = options or {}
        self.stats = {"processed": 0, "ignored": 0}
        # Threshold for warning (500 KB)
        self.size_threshold = 500 * 1024

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
        all_files = []
        for root, _, files in os.walk(self.repo_path):
            for name in files:
                all_files.append(os.path.join(root, name))

        with self.display.progress_context() as progress:
            task = progress.add_task("[cyan]Processing repository...", total=len(all_files))

            for full_path in all_files:
                rel_path = os.path.relpath(full_path, self.repo_path)

                if self.im.should_ignore(rel_path):
                    self.stats["ignored"] += 1
                    progress.advance(task)
                    continue

                if self.options.get('skip_binary', True) and self.is_binary(full_path):
                    self.stats["ignored"] += 1
                    progress.advance(task)
                    continue

                file_size = os.path.getsize(full_path)
                max_size_kb = self.options.get('max_size')
                if max_size_kb is not None:
                    if file_size > (max_size_kb * 1024):
                        self.display.warning(f"Skipping {rel_path}: size {round(file_size/1024, 1)}KB exceeds limit ({max_size_kb}KB)")
                        self.stats["ignored"] += 1
                        progress.advance(task)
                        continue
                else:
                    if file_size > self.size_threshold:
                        size_kb = round(file_size / 1024, 2)
                        self.display.warning(f"{rel_path} is large ({size_kb} KB)")

                try:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    if rel_path.endswith(".ipynb"):
                        content = self.clean_notebook(content)

                    output_file.write(f"----\n{rel_path}\n{content}\n")
                    self.stats["processed"] += 1
                except Exception:
                    self.stats["ignored"] += 1
                
                progress.advance(task)