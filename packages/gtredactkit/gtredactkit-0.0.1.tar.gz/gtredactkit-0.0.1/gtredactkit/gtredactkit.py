#!/usr/bin/env python
"""
Utility to redact sensitive data
"""

import argparse
from gtredactkit.redact import Redactor
from gtredactkit.unredact import Unredactor
import os
import glob

banner = r"""

  ________ __    __________           .___              __     ____  __.__  __   
 /  _____//  |_  \______   \ ____   __| _/____    _____/  |_  |    |/ _|__|/  |_ 
/   \  __\   __\  |       _// __ \ / __ |\__  \ _/ ___\   __\ |      < |  \   __\
\    \_\  \  |    |    |   \  ___// /_/ | / __ \\  \___|  |   |    |  \|  ||  |  
 \______  /__|    |____|_  /\___  >____ |(____  /\___  >__|   |____|__ \__||__|  
        \/               \/     \/     \/     \/     \/               \/                                                                                   
                    +-+-+-+-+-+-+-+ +-+-+ +-+-+-+-+-+-+-+-+-+
                    |P|o|w|e|r|e|d| |b|y| |B|r|o|o|t|w|a|r|e|
                    +-+-+-+-+-+-+-+ +-+-+ +-+-+-+-+-+-+-+-+-+
            
    https://github.com/brootware
    https://brootware.github.io                                                                             
    """


def main():
    print(banner)

    parser = argparse.ArgumentParser(
        description='Read in a file or set of files, and return the result.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "file",
        nargs="+",
        help="""
        Path of a file or a directory of files.
        Usage: gtredactkit [file/filestoredact]"""
    )
    parser.add_argument(
        "-u",
        "--unredact",
        help="""
        Option to unredact masked data.
        Usage: gtredactkit [redacted_file] -u [.hashshadow.json]
        """
    )
    parser.add_argument(
        "-t", "--redactiontype",
        help="""Type of data to redact. 
        names,
        nric,
        dns,
        emails,
        ipv4,
        ipv6,
        base64.
        Usage: gtredactkit [file/filestoredact] -t ip"""
    )
    parser.add_argument(
        "-d",
        "--dirout",
        help="""
        Output directory of the file.
        Usage: gtredactkit [file/filestoredact] -d [redacted_dir]
        """
    )
    parser.add_argument(
        '-r',
        '--recursive',
        action='store_true',
        default=True,
        help='Search through subfolders'
    )
    parser.add_argument(
        '-e',
        '--extension',
        default='',
        help='File extension to filter by.'
    )
    args = parser.parse_args()

    full_paths = [os.path.join(os.getcwd(), path) for path in args.file]
    files = set()

    for path in full_paths:
        if os.path.isfile(path):
            file_name, file_ext = os.path.splitext(path)
            if args.extension in ('', file_ext):
                files.add(path)
        elif args.recursive:
            full_paths += glob.glob(path + '/*')

    # redact file
    redact_obj = Redactor()
    unredact_obj = Unredactor()

    for file in files:
        if args.redactiontype:
            redact_obj.process_file(file, args.redactiontype)
        elif args.dirout:
            redact_obj.process_file(file, args.redactiontype, args.dirout)
            redact_obj.process_report(file, args.dirout)
        elif args.unredact:
            unredact_obj.unredact(file, args.unredact)
        else:
            redact_obj.process_file(file)
            redact_obj.process_report(file)


if __name__ == "__main__":
    main()
