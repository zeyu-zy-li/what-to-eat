import argparse
from repo import *


# This function will accept the arguments from the CLI
def main():
    obj = SqliteRepository('recipe.db')
    parser = argparse.ArgumentParser()
    # one of add, delete and check would be True depends on the -a, -d or -c
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a', '--add', action='store_true')
    group.add_argument('-d', '--delete', action='store_true')
    group.add_argument('-q', '--query', action='store_true')
    group.add_argument('-l', '--list', action='store_true')
    group.add_argument('-u', '--update', action='store_true')
    # The string after -n would be assigned to name
    parser.add_argument('-n', '--name', type=str)
    # The other arguments would be stored in the ingredients
    parser.add_argument('ingredients', nargs="*", action='store')
    args = parser.parse_args()
    # print("add", args.add)
    # print("delete", args.delete)
    # print("list", args.list)
    # print("update", args.update)
    # print("name", args.name)
    # print("check", args.query)
    # print("ingredients", args.ingredients)


    # python3 currentFile.py -a -n KongpoChicken chicken peanut
    # The above will add a recipe "kongpochicken" in table Recipe and ingredients "chicken"
    # and "peanut" in table "Ingredient" and the relation in table Recipe_Ingredient.
    # Note that if the ingredient has been in the table, it would not insert again.
    # If the recipe has been in the table, it would insert nothing and print the prompt.
    if args.add:
        try:
            obj.add_recipe(args.name.lower(), args.ingredients)
            print("Dish {} is added successfully.".format(args.name.lower()))
        except DishExistsError:
            print("This dish has been added in the Recipe before. Please use -u to update it.")
    # python3 currentFile.py -q chicken peanut onion
    # The above will check which dish can be cooked with these ingredients.
    # It would print ('kongpochicken', 'chicken, peanut') like ('dish', 'food1,food2,food3,...').
    elif args.query:
        print(obj.check_food(args.ingredients))
    # python3 currentFile.py -l -n kongpoChicken
    # The above will read the ingredients of this dish
    # It would print ('kongpochicken', 'chicken,peanut') like ('dish', 'food1,food2,food3,...').
    # python3 currentFile.py -l
    # It will list all the dish names in Recipe
    elif args.list:
        if args.name:
            print(obj.list_recipe(args.name.lower()))
        else:
            print(obj.list_recipes())
    # python3 currentFile.py -d -n KongpoChicken
    # The above will delete the recipe "kongpochicken" and the relative rows in the table Recipe_Ingredient.
    # The table Ingredient would not be changed.
    # If there is no recipe with this name, it will do nothing but print the prompt.
    elif args.delete:
        try:
            obj.delete_recipe(args.name.lower())
            print("{} has been deleted".format(args.name.lower()))
        except DishNotExistsError:
            print("There is no recipe for this dish.")
    # python3 currentFile.py -u -n kongPoChicken chicken carrot onion cucumber
    # It will check if "kongpochickent" exists in Recipe.
    # If not, it will return the prompt.
    # If so, it will update the ingredients of this dish.
    elif args.update:
        try:
            obj.update_recipe(args.name.lower(), args.ingredients)
            print("Dish '{}' has been updated.".format(args.name.lower()))
        except DishNotExistsError:
            print("There is no dish '{}'. If you want to add it, please use -a to add.".format(args.name.lower()))


if __name__ == "__main__":
    main()
