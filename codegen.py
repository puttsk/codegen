import sys
import argparse
import json
from parser.block import Block

def init_arg_parsers() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Convert input data to an output file based on template')
    parser.add_argument('-d','--data',metavar='PATH',type=str,help='path to data file')
    parser.add_argument('-o','--output',type=str,help='output file name')
    parser.add_argument('-t','--template',type=str,help='path to template file')
    return parser

def main():
    parser = init_arg_parsers()
    args = parser.parse_args()

    try:
        with open(args.data, mode='r') as f:
            data = json.load(f)
    except:
        print("Invalid data path")
        parser.print_help()

    b = Block()
    # Convert template file to internal building block
    try: 
        with open(args.template, mode='r') as t:      
            b.read_block(t)
    except FileNotFoundError as err:
        print("Cannot open template file %s".format(err.filename))
    except Exception as err:
        print("Unexpected error %s", err)
        sys.exit(1)
    
    # Generate output
    try: 
        with open(args.output, mode='w') if args.output else sys.stdout as o:      
            b.process(data, o)
    except FileNotFoundError as err:
        print("Cannot open template file %s".format(err.filename))
    except Exception as err:
        print("Unexpected error %s", err)
        sys.exit(1)


if __name__ == "__main__":
    main()