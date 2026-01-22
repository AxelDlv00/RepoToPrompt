import argparse
import sys
import os
from .display import Display
from .utils import IgnoreManager
from .core import RepoProcessor

def main():
    display = Display()
    parser = argparse.ArgumentParser(prog="RepoToPrompt", add_help=False)
    
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--init-ignore", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("-o", "--output", default="output.txt")
    parser.add_argument("--max-size", type=int, help="Max file size in KB to include (e.g., 100).")
    parser.add_argument("-h", "--help", action="store_true")
    
    args = parser.parse_args()

    if args.help:
        display.show_help()
        sys.exit(0)

    if not os.path.exists(args.path):
        display.error(f"Path not found: {args.path}")
        sys.exit(1)

    display.banner()
    im = IgnoreManager(args.path)

    if args.init_ignore:
        if im.create_default_ignore(force=args.force):
            display.success("Created .RepoToPromptignore file.")
        else:
            display.info("Ignore file already exists. Use --force to overwrite.")
        sys.exit(0)

    im.load_patterns()
    processor = RepoProcessor(args.path, im, display, {'skip_binary': True, 'max_size': args.max_size})
    
    try:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write("The following text is a repository with code...\n")
            processor.process(f)
            f.write("--END--\n")
        
        display.summary(processor.stats, args.output)
        display.success("Repository successfully consolidated.")
    except Exception as e:
        display.error(f"Failed to write output: {e}")

if __name__ == "__main__":
    main()