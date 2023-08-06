#!/usr/bin/env python

import argparse

from pybsc import load_json
from pybsc import save_json


def main():
    parser = argparse.ArgumentParser(description='Reformat json')
    parser.add_argument('input_json', type=str, help='Input json file')
    parser.add_argument('output_json', type=str, help='Output json file')
    args = parser.parse_args()

    data = load_json(args.input_json)
    save_json(data, args.output_json)


if __name__ == '__main__':
    main()
