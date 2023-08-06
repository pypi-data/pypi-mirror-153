import io
import requests
import argparse
import pandas as pd

from parsers import parse_json, parse_csv

def main(args):

    response = requests.get("https://randomuser.me/api/", params=vars(args))

    if args.format == "json":
        response_json = parse_json(response)
        print(response_json)

    elif args.format == "csv":
        response_df = parse_csv(response)
        print(response_df)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--gender', type=str,
                        help='User gender')
    parser.add_argument('--nationality', type=str, default='br',
                        help='User nationality')
    parser.add_argument('--format', type=str, default='json',
                        help='Output format: json or csv')
    args = parser.parse_args()
    main(args)
