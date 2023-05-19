# cli.py

import argparse

def read_user_cli_input():
    """Get CLI arguments and options"""
    parser = argparse.ArgumentParser(
        prog="sitecheck", description="Check if a website is available"
    )
    parser.add_argument(
        # -u and --urls switches
        "-u",
        "--urls",
        # Metavar sets the name of the argument in usage or help messages
        metavar="URLs",
        # List of cli arguments after the -u and --urls switch
        nargs="+",
        type=str,
        # Sets arguments to an empty list by default
        default=[],
        help="Enter one or more website URLs"
    )
    parser.add_argument(
        "-f",
        "--input-file",
        metavar="FILE",
        type=str,
        default="",
        help="Read URLs from a file",
    )
    parser.add_argument(
        "-a",
        "--asynchronous",
        action="store_true",
        help="Run the connectivity check asynchronously"
    )
    return parser.parse_args()

def display_check_result(result, url, error=""):
    # Display the result of a connectivity check.
    print(f'The status of "{url}" is:', end=" ")
    if result:
        print('"Online!" 👍')
    else:
        print(f'"Offline?" 👎 \n Error: "{error}"')