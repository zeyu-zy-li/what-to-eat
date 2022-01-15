import argparse

parser = argparse.ArgumentParser(description = "An addition parogram")

parser.add_argument("add", nargs = "*", metavar = "num", type = int, help = "add all numbers")

args = parser.parse_args()
print(args)
print(args.add)
if len(args.add) != 0:
    print(sum(args.add))
