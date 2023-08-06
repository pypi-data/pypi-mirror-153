import argparse
from enclosed import Parser, is_enclosed


def main():
    parser = argparse.ArgumentParser(description="Extract enclosed tokens from string")
    parser.add_argument(
        "target",
        metavar="target",
        type=str,
        help="full string containing enclosed tokens",
    )
    args = parser.parse_args()
    tokens_parser = Parser()
    tokens = tokens_parser.tokenize(args.target)
    enclosed_strs = [token[2] for token in tokens if is_enclosed(token)]
    print(" ".join(enclosed_strs))


if __name__ == "__main__":
    main()
