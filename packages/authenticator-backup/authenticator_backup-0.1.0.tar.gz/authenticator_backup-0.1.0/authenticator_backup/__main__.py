import argparse
import sys

from authenticator_backup.backup import backup
from authenticator_backup.restore import restore


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Backup Google Authenticator")
    parser.add_argument(
        "--gnupg-home", dest="gnupghome", type=str, help="GPG home directory"
    )

    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand")

    backup_parser = subparsers.add_parser("backup")
    backup_parser.add_argument(
        "recipients",
        metavar="RECIPIENT",
        type=str,
        nargs="+",
        help="GPG/PGP public key recipients",
    )
    backup_parser.add_argument(
        "-o", "--outfile", type=str, help="Output file (defualt: stdout)"
    )

    restore_parser = subparsers.add_parser("restore")
    restore_parser.add_argument(
        "--infile", type=str, help="Input file (defualt: stdin)"
    )

    return parser.parse_args()


def main(argv):
    args = parse_args(argv)

    if args.subcommand == "backup":
        backup(args.recipients, outfile=args.outfile, gnupghome=args.gnupghome)
    elif args.subcommand == "restore":
        restore(infile=args.infile, gnupghome=args.gnupghome)
    else:
        raise ValueError(f"Unknown commnad: {command}")


if __name__ == "__main__":
    main(sys.argv[1:])
