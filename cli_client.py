import requests
import argparse


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a', '--add', action='store_true')
    group.add_argument('-d', '--delete', action='store_true')
    group.add_argument('-q', '--query', action='store_true')
    group.add_argument('-l', '--list', action='store_true')
    group.add_argument('-u', '--update', action='store_true')
    parser.add_argument('-n', '--name', type=str)
    parser.add_argument('ingredients', nargs="*", action='store')
    args = parser.parse_args()

    if args.add:
        response = requests.post("http://127.0.0.1:5000/recipes", json={"dish": args.name.lower(), "ingredients": args.ingredients})
        if response.status_code == 200:
            print("Dish {} is added successfully.".format(args.name.lower()))
        elif response.status_code == 409:
            print("This dish has been added in the Recipe before. Please use -u to update it.")
        else:
            print("There is something wrong.")
    elif args.query:
        response = requests.post("http://127.0.0.1:5000/recipes/check", json={"ingredients": args.ingredients})
        print(response.text)
    elif args.list:
        if args.name:
            response = requests.get("http://127.0.0.1:5000/recipe/{}".format(args.name.lower()))
            print(response.text)
        else:
            response = requests.get("http://127.0.0.1:5000/recipes")
            print(response.text)
    elif args.delete:
        response = requests.delete("http://127.0.0.1:5000/recipe/{}".format(args.name.lower()))
        if response.status_code == 200:
            print("{} has been deleted".format(args.name.lower()))
        elif response.status_code == 404:
            print("There is no recipe for this dish.")
        else:
            print("There is something wrong.")
    elif args.update:
        response = requests.put("http://127.0.0.1:5000/recipe/{}".format(args.name.lower()), json={"ingredients": args.ingredients})
        if response.status_code == 200:
            print("Dish '{}' has been updated.".format(args.name.lower()))
        elif response.status_code == 404:
            print("There is no dish '{}'. If you want to add it, please use -a to add.".format(args.name.lower()))
        else:
            print("There is something wrong.")


if __name__ == "__main__":
    main()
