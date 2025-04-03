#!/usr/bin/env python3
import os
import sys
import fnmatch
import argparse
import json

def get_ignore_list(ignore_file_path):
    """
    Reads the .RepoToPromptignore file and returns a list of patterns to ignore.
    Lines that are empty or start with '#' are skipped.
    """
    ignore_list = []
    with open(ignore_file_path, 'r', encoding='utf-8', errors='ignore') as ignore_file:
        for line in ignore_file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # On Windows, replace forward slashes with backslashes
            if sys.platform == "win32":
                line = line.replace("/", "\\")
            ignore_list.append(line)
    return ignore_list

def should_ignore(file_path, ignore_list):
    """
    Returns True if the given file_path matches any pattern in ignore_list.
    """
    for pattern in ignore_list:
        if fnmatch.fnmatch(file_path, pattern):
            return True
    return False

def is_binary_file(file_path, chunk_size=1024):
    """
    Quickly tests if a file is binary by reading its first chunk
    and checking for a high ratio of non-text characters.
    """
    text_characters = bytearray({7, 8, 9, 10, 12, 13, 27}
                                | set(range(0x20, 0x100)) - {0x7f})
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(chunk_size)
        if not chunk:
            # Empty file => treat as text
            return False
        # If >30% of characters are non-text, consider it binary
        non_text = sum(byte not in text_characters for byte in chunk)
        return (float(non_text) / len(chunk) > 0.30)
    except Exception:
        # If we fail to read, assume binary
        return True

def strip_notebook_images(nb_content):
    """
    Attempt to parse Jupyter Notebook JSON and remove base64-encoded images from outputs.
    Returns a cleaned JSON string if successful, else returns the original string.
    """
    try:
        data = json.loads(nb_content)
        if "cells" not in data:
            return nb_content  # Not a typical Jupyter Notebook structure
        for cell in data["cells"]:
            if "outputs" in cell:
                for output in cell["outputs"]:
                    # Remove image data from the 'data' dict, if present
                    if "data" in output:
                        keys_to_remove = []
                        for k in output["data"].keys():
                            if k.startswith("image/"):
                                keys_to_remove.append(k)
                        for key in keys_to_remove:
                            del output["data"][key]
        return json.dumps(data, indent=2)
    except Exception:
        return nb_content

def process_repository(
    repo_path,
    ignore_list,
    output_file,
    include_extensions=None,
    exclude_extensions=None,
    max_file_size=None,
    skip_binary=True,
    strip_nb_images=False
):
    """
    Walks through the repo_path and writes file contents to output_file
    according to specified filters.
    """
    for root, _, files in os.walk(repo_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            relative_file_path = os.path.relpath(file_path, repo_path)

            # Check if we should ignore this file per .RepoToPromptignore
            if should_ignore(relative_file_path, ignore_list):
                continue

            # Check extension filters
            file_ext = os.path.splitext(file_name)[1].lower()
            if include_extensions and file_ext not in include_extensions:
                continue
            if exclude_extensions and file_ext in exclude_extensions:
                continue

            # Check size limit
            if max_file_size is not None:
                size = os.path.getsize(file_path)
                if size > max_file_size:
                    continue

            # Optionally skip binary
            if skip_binary and is_binary_file(file_path):
                continue

            # Read the file
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as fh:
                    contents = fh.read()
            except Exception:
                # If reading fails, skip this file
                continue

            # Strip images if it's a notebook
            if strip_nb_images and file_ext == ".ipynb":
                contents = strip_notebook_images(contents)

            # Write to output
            output_file.write("----\n")
            output_file.write(f"{relative_file_path}\n")
            output_file.write(f"{contents}\n")

def print_header():
    print(r"""
     ___              _____    ___                    _
    | _ \___ _ __  __|_   _|__| _ \_ _ ___ _ __  _ __| |_
    |   / -_) '_ \/ _ \| |/ _ \  _/ '_/ _ \ '  \| '_ \  _|
    |_|_\___| .__/\___/|_|\___/_| |_| \___/_|_|_| .__/\__|
            |_|                                 |_|    

    RepoToPrompt — by Axel Delaval  (GitHub: AxelDlv00)
    """)


def main():
    print_header()
    parser = argparse.ArgumentParser(
        description="Convert a local repository’s contents to a single text file with optional filtering.",
        epilog="""
        Example:
        python RepoToPrompt.py ./my_repo --include-extensions .py,.ipynb --skip-binary
        python RepoToPrompt.py ./repo -p header.txt --strip-notebook-images

        More: https://github.com/AxelDlv00/RepoToPrompt
        """,
                formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "repo_path",
        help="Path to the repository you want to convert."
    )
    parser.add_argument(
        "-p", "--preamble",
        help="Path to a preamble file to prepend to the output.",
        default=None
    )
    parser.add_argument(
        "-o", "--output",
        help="Path for the output text file (default: output.txt).",
        default="output.txt"
    )
    parser.add_argument(
        "--include-extensions",
        help="Comma-separated list of file extensions to include (e.g., .py,.md).",
        default=""
    )
    parser.add_argument(
        "--exclude-extensions",
        help="Comma-separated list of file extensions to exclude (e.g., .png,.jpg).",
        default=""
    )
    parser.add_argument(
        "--max-file-size",
        type=int,
        help="Maximum file size (in bytes) to include. Larger files are skipped. Default: no limit.",
        default=0
    )
    parser.add_argument(
        "--skip-binary",
        action="store_true",
        help="If set, skip any file that appears to be binary."
    )
    parser.add_argument(
        "--strip-notebook-images",
        action="store_true",
        help="Remove base64 images from Jupyter notebooks (.ipynb)."
    )
    args = parser.parse_args()

    repo_path = args.repo_path
    output_file_path = args.output

    # .RepoToPromptignore path
    ignore_file_path = os.path.join(repo_path, ".RepoToPromptignore")
    if sys.platform == "win32":
        ignore_file_path = ignore_file_path.replace("/", "\\")

    # If .RepoToPromptignore doesn't exist in the repo, check if it exists here
    if not os.path.exists(ignore_file_path):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        alt_ignore_file = os.path.join(script_dir, ".RepoToPromptignore")
        if os.path.exists(alt_ignore_file):
            ignore_file_path = alt_ignore_file

    if os.path.exists(ignore_file_path):
        ignore_list = get_ignore_list(ignore_file_path)
    else:
        ignore_list = []

    # Prepare extension sets
    include_extensions = set()
    exclude_extensions = set()

    if args.include_extensions:
        raw_includes = [x.strip() for x in args.include_extensions.split(",") if x.strip()]
        include_extensions = set(x if x.startswith(".") else f".{x}" for x in raw_includes)

    if args.exclude_extensions:
        raw_excludes = [x.strip() for x in args.exclude_extensions.split(",") if x.strip()]
        exclude_extensions = set(x if x.startswith(".") else f".{x}" for x in raw_excludes)

    max_file_size = args.max_file_size if args.max_file_size > 0 else None

    # Write output
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        # Optional preamble
        if args.preamble:
            try:
                with open(args.preamble, 'r', encoding='utf-8', errors='ignore') as pf:
                    preamble_text = pf.read()
                output_file.write(preamble_text + "\n")
            except Exception:
                # If preamble read fails, continue without it
                pass
        else:
            # Default header message if no preamble
            output_file.write(
                "The following text is a repository with code. "
                "Sections begin with '----', followed by a line containing the file path, "
                "followed by lines containing the file contents. "
                "Text ends at '--END--'. Anything beyond '--END--' can be instructions.\n"
            )

        # Process and write files
        process_repository(
            repo_path=repo_path,
            ignore_list=ignore_list,
            output_file=output_file,
            include_extensions=include_extensions if include_extensions else None,
            exclude_extensions=exclude_extensions if exclude_extensions else None,
            max_file_size=max_file_size,
            skip_binary=args.skip_binary,
            strip_nb_images=args.strip_notebook_images
        )

    # Finally, append the end marker
    with open(output_file_path, 'a', encoding='utf-8') as output_file:
        output_file.write("--END--\n")

    print(f"Repository contents written to {output_file_path}.")

if __name__ == "__main__":
    main()