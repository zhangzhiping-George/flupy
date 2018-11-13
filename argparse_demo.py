import argparse

parser = argparse.ArgumentParser(description="your script description")
parser.add_argument('--verbose', '-v', required=True, action='store_true', help='verbose mode')
args = parser.parse_args() 
#print(list(dir(args)))
if args.verbose:
    print("Verbose mode on!")
else:
    print("Verbose mode off!")
