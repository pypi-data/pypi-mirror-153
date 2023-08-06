import ssl
import sys
from argparse import ArgumentParser, Namespace
from http.client import RemoteDisconnected
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


def eprint(*values: object):
    print(*values, file=sys.stderr)


def parse_args():
    parser = ArgumentParser(description="Health check website")
    parser.add_argument(
        "url", type=str,
        help="url to query for status"
    )
    parser.add_argument(
        "--timeout", dest="timeout",
        type=float, default=0.3,
        help="timeout before connection fail"
    )
    parser.add_argument(
        "--allow-unverified", action="store_true",
        help="allows for invalid self-signed certificates to be valid"
    )
    return parser.parse_args()


def main(args: Namespace):
    ssl_context = None
    if args.allow_unverified:
        ssl_context = ssl._create_unverified_context()

    try:
        with urlopen(
            args.url,
            timeout=args.timeout,
            context=ssl_context,
        ) as response:
            if response.read().decode() != "🆗":
                eprint(f"⛔ missing '🆗' in response")
            else:
                print("🆗")
                return
    except HTTPError as err:
        eprint(f"⛔ http status '{err.code}'")
    except URLError as err:
        eprint(f"⛔ url error '{err.reason}'")
    except RemoteDisconnected:
        eprint(f"⛔ remote closed without response")

    exit(1)


if __name__ == "__main__":
    args = parse_args()
    main(args)
