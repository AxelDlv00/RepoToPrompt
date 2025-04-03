```
  ___              _____    ___                    _
 | _ \___ _ __  __|_   _|__| _ \_ _ ___ _ __  _ __| |_
 |   / -_) '_ \/ _ \| |/ _ \  _/ '_/ _ \ '  \| '_ \  _|
 |_|_\___| .__/\___/|_|\___/_| |_| \___/_|_|_| .__/\__|
         |_|                                 |_|    
```

# RepoToPrompt

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Repository](https://img.shields.io/badge/GitHub-View%20Source-blue?logo=github)](https://github.com/AxelDlv00/RepoToPrompt)

---

## Overview

**RepoToPrompt** is a tool that converts a repository into a single, structured plain-text document. It allows fine-grained filtering of included files and formatting to suit AI prompting, auditing, and archival needs.

> Inspired by [gpt-repository-loader](https://github.com/mpoon/gpt-repository-loader), and partially restructured to support more flexible extension control, binary skipping, and notebook image filtering, which substantially impact the quality of LLM's answers.

---

## Features

- Filter files by **include/exclude extensions**
- Ignore files using a **`.RepoToPromptignore`** (similar to `.gitignore`)
- Automatically **strip base64 image blobs** from Jupyter Notebooks
- Automatically **skip binary files** and large files
- Configurable **output preamble** and file format

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/AxelDlv00/RepoToPrompt.git
cd RepoToPrompt
```

### 2. Requirements

RepoToPrompt only requires **Python 3**.  
You can install Python from your system’s package manager or from [Python.org](https://www.python.org/) directly.  
Alternatively, you can use a conda environment, e.g.:

```bash
conda create -n repotoprompt python=3.9
conda activate repotoprompt
```

### 3. (Optional) Add the Script to Your PATH

If you use **bash**:

```bash
echo "export PATH=\"$(pwd):\$PATH\"" >> ~/.bashrc
source ~/.bashrc
```

Now you can call `RepoToPrompt.py` from anywhere.

---

## Usage

```bash
python RepoToPrompt.py /path/to/repo \
  [--preamble preamble.txt] \
  [--output output.txt] \
  [--include-extensions .py,.ipynb] \
  [--exclude-extensions .jpg,.png] \
  [--max-file-size 100000] \
  [--skip-binary] \
  [--strip-notebook-images]
```

Parameters:

- `repo_path`: Path to the repository you want to convert.
- `--preamble`: Path to a text file whose content will be prepended to the output.
- `--output`: Output file path (default: `output.txt`).
- `--include-extensions`: Comma-separated list of file extensions to include (e.g., `.py,.md`).
- `--exclude-extensions`: Comma-separated list of file extensions to exclude (e.g., `.jpg,.png`).
- `--max-file-size`: Skip files larger than this size (in bytes).
- `--skip-binary`: Skip files that appear to be binary.
- `--strip-notebook-images`: Remove base64 images from Jupyter notebooks.

### Example

```bash
python RepoToPrompt.py ./my_repo \
  --preamble my_preamble.txt \
  --output consolidated_repo.txt \
  --include-extensions .py,.ipynb \
  --exclude-extensions .png,.jpg \
  --max-file-size 100000 \
  --skip-binary \
  --strip-notebook-images
```

---

## Output Format

```
----
relative/path/to/file.ext
<file contents>
----
relative/path/to/another_file.ext
<file contents>
--END--
<Instructions or additional text beyond this point>
```

---

## .RepoToPromptignore

A simple ignore file that works like `.gitignore`. Example content:

```
*.log
__pycache__/
data/
*.png
*.jpg
*.pdf
*.aux
*.bbl
*.fdb_latexmk
*.fls
*.log
*.out
*.synctex.gz
*.toc
*.DS_Store
*.git*
*.txt
```

Place it in the root of the repo (or next to the script) to filter out files or folders you don’t want included.

---

## License

MIT License — see [LICENSE](LICENSE).

This project reuses logic and structure from [gpt-repository-loader](https://github.com/mpoon/gpt-repository-loader).

---

## Author

- Axel Delaval

--- 

- Last update : March 2025
