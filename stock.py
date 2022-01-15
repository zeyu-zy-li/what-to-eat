import argparse, sys
stockFood = set()
def add(args):
    for arg in args:
        stockFood.add(arg)
def show():
    print(stockFood)
def delete(args):
    for arg in args:
        if arg in stockFood:
            stockFood.remove(arg)
        else:
            print("No", arg)

def main():
    parser = argparse.ArgumentParser(description = "A program for stock of food")
    
    # parser.add_argument(
    #     "add", nargs = "*", metavar = "food", type = str, help = "add all food")
    # parser.add_argument(
    #     "show", 
    # )
    #print(sys.argv)
    # args = parser.parse_args()
    # print(args.add)
    show()
    if (sys.argv[1] == "add"):
        print(sys.argv)
        add(sys.argv[2:])
        show()


if __name__ == "__main__":
    main()