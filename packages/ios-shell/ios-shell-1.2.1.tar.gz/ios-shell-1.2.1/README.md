# IOS Shell file parsing library

This is a library for parsing files in the IOS Shell format.
It has no relation to iOS or terminal shells.

## Prerequisites

- Python 3.8, 3.9, or 3.10 with pip

## Example

If `1930-003-0058.bot` is in the same folder as the program using ios_shell:

    parsed_file = ios_shell.ShellFile.fromfile("1930-003-0058.bot")

To use the contents of a file previously read into the program:

    parsed_contents = ios_shell.ShellFile.fromcontents(contents)
