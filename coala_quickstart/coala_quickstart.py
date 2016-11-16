import argparse
import os
import sys

from pyprint.ConsolePrinter import ConsolePrinter

from coalib.output.printers.LogPrinter import LogPrinter

from coala_utils.Question import ask_question

from coala_quickstart.interaction.Logo import print_welcome_message
from coala_quickstart.generation.Project import (
    valid_path, get_used_languages, print_used_languages)
from coala_quickstart.generation.FileGlobs import get_project_files
from coala_quickstart.generation.Bears import (
    filter_relevant_bears, print_relevant_bears)
from coala_quickstart.generation.Settings import (
    generate_settings, write_coafile)


def main():
    description = """
coala-quickstart automatically creates a .coafile for use by coala.
"""

    arg_parser = argparse.ArgumentParser(
        prog="coala-quickstart",
        description=description,
        add_help=True
    )

    arg_parser.add_argument(
        '--non-interactive', const=True, action='store_const',
        help='run in automatic mode without asking any questions.')

    args = arg_parser.parse_args()

    printer = ConsolePrinter()
    log_printer = LogPrinter(printer)

    print_welcome_message(printer)

    project_dir = os.getcwd()
    if not args.non_interactive:
        project_dir = ask_question(
            "What is your project directory?",
            default=project_dir,
            typecast=valid_path)

    project_files, ignore_globs = get_project_files(
        log_printer,
        printer,
        project_dir)

    used_languages = list(get_used_languages(project_files))
    print_used_languages(printer, used_languages)

    relevant_bears = filter_relevant_bears(
        used_languages,
        arg_parser=arg_parser,
        optional_settings=not args.non_interactive)

    print_relevant_bears(printer, relevant_bears)

    settings = generate_settings(
        project_dir,
        project_files,
        ignore_globs,
        relevant_bears)
    write_coafile(printer, project_dir, settings)
