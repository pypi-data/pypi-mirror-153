import os
import argparse
import re

from FlintCLN.FlintCLN import FlintCLN

def run():
    """
    """

    # Retrieves the arguments provided on the command-line.
    parser = argparse.ArgumentParser(description="This script will perform linting of Ficklin Program project repositories.")

    parser.add_argument("--project_dir", dest="project_dir", type=str,
        default="", required=True, help="Required.  Specify the directory where the project repository resides.")
    parser.add_argument("--summary", dest="summary", action='store_false',
        default=True, required=False, help="Indicates if the lint output should be only a summary and not exact problems.")

    args = parser.parse_args()

    # If this is a relative path then update it to include the full path
    project_dir = args.project_dir
    regexp = re.compile(r"^[^\/]")
    if regexp.search(project_dir):
        project_dir = os.path.join(os.getcwd(), project_dir)

    flint = FlintCLN(project_dir, verbose=args.summary)
    flint.addIgnorePattern(r"^work$")
    flint.run()
    flint.printErrors()
    flint.printWarnings()
