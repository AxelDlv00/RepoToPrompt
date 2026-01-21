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

**RepoToPrompt** is a CLI tool that converts a local repository into a single, structured plain-text document optimized for AI context windows. It automatically handles binary file skipping and Jupyter Notebook cleaning to provide high-quality prompts.

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/AxelDlv00/RepoToPrompt.git
cd RepoToPrompt
```

### 2. Install as a package

Use the editable mode to install the `RepoToPrompt` command globally in your environment:

```bash
pip install -e .
```

*Note: This will automatically install dependencies like `rich`.*

---

## Usage

### Initialize Ignore File

Generate a default ignore file populated with common patterns (logs, binaries, etc.):

```bash
RepoToPrompt --init-ignore
```

Or manually create a `.RepoToPromptignore` file in your repository root.

*Use `--force` to overwrite an existing ignore file.*

### Convert a Repository

```bash
RepoToPrompt [path/to/repo] [options]
```

**Options:**

* `path`: Path to the repository (default is current directory `.`).
* `-o, --output`: Name of the output text file (default: `output.txt`).
* `--init-ignore`: Create the default `.RepoToPromptignore` file.
* `--force`: Force overwrite of the ignore file during initialization.
* `-h, --help`: Show the styled help page.

### Example

```bash
RepoToPrompt ./my-project -o my_prompt.txt
```

---

## .RepoToPromptignore

Place this file in your root directory to exclude specific files or folders. Example:

```text
# Folders
.git/
node_modules/
venv/

# Files
*.png
*.pdf
secret.env
```

---

## Output Format

The generated file follows a structured format that LLMs easily understand:

```text
The following text is a repository with code...
----
relative/path/to/file.py
<file contents>
----
relative/path/to/script.js
<file contents>
--END--
```

---

## License

MIT License — see [LICENSE](https://www.google.com/search?q=LICENSE).

---

## Author

* **Axel Delaval** - [AxelDlv00](https://github.com/AxelDlv00)

---

* Last update : January 2026