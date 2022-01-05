#!/usr/bin/env python
import json
from src.metrics.avg_sentence_length import get

if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description='Get average sentence length from a file.')
    parser.add_argument('filename', help='filename', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    args = parser.parse_args()
    results = get(args.filename.read())
    sys.stdout.write(json.dumps(results))

