import argparse
import sys
import sqlite3


class SqliteRepository:
    sql_dish_count = "SELECT COUNT(dish) FROM Recipe WHERE dish = '{}';"
    sql_dish_insert = "INSERT INTO Recipe(dish) VALUES('{}');"
    sql_dish_id = "SELECT ID FROM Recipe WHERE dish = '{}';"
    sql_food_count = "SELECT COUNT(food) FROM Ingredient WHERE food = '{}';"
    sql_food_insert = "INSERT INTO Ingredient(food) VALUES('{}');"
    sql_food_id = "SELECT ID FROM Ingredient WHERE food = '{}';"
    sql_dish_food_insert = "INSERT INTO Recipe_Ingredient(Recipe_ID, Ingredient_ID) VALUES ({}, {});"
    sql_dish_id_count = "SELECT ID, COUNT(ID) FROM Recipe WHERE dish = '{}';"
    sql_dish_food_delete = "DELETE FROM Recipe_Ingredient WHERE Recipe_ID = {};"
    sql_dish_delete = "DELETE FROM Recipe WHERE ID = {};"
    sql_dish_food_all = "SELECT dish, group_concat(food) FROM Recipe JOIN Recipe_Ingredient ON Recipe.ID = Recipe_Ingredient.Recipe_ID JOIN Ingredient ON Recipe_Ingredient.Ingredient_ID = Ingredient.ID GROUP BY dish;"
    sql_dish_food_one = "SELECT dish, group_concat(food) FROM Recipe JOIN Recipe_Ingredient ON Recipe.ID = Recipe_Ingredient.Recipe_ID JOIN Ingredient ON Recipe_Ingredient.Ingredient_ID = Ingredient.ID WHERE dish = '{}' GROUP BY dish;"
    sql_dish_all = "SELECT dish FROM Recipe;"

    def __init__(self):
        pass
        # self.con = sqlite3.connect(db_name)  , db_name
        # self.cur = self.con.cursor()

    # add recipe with the "dishName" and [ingredients]
    def add_recipe(self, dish_name, ingredients):
        try:
            con = sqlite3.connect('test3.db')
            cur = con.cursor()
            if cur.execute(self.sql_dish_count.format(dish_name)).fetchone()[0] == 0:
                cur.execute(self.sql_dish_insert.format(dish_name))
            else:
                return "This dish has been added in the Recipe before. Please use -u to update it."

            recipe_id = cur.execute(self.sql_dish_id.format(dish_name)).fetchone()[0]
            for ingredient in ingredients:
                if cur.execute(self.sql_food_count.format(ingredient)).fetchone()[0] == 0:
                    cur.execute(self.sql_food_insert.format(ingredient))
                ingredient_id = cur.execute(self.sql_food_id.format(ingredient)).fetchone()[0]
                cur.execute(self.sql_dish_food_insert.format(recipe_id, ingredient_id))
            return "This dish is added successfully."
        except sqlite3.Error as e:
            print("Error: '{}'".format(e.args[0]))
            sys.exit(1)
        finally:
            if con:
                con.commit()
                con.close()

    # delete the recipe with the name of "dishName"
    def delete_recipe(self, dish_name):
        con = sqlite3.connect('test3.db')
        with con:
            cur = con.cursor()
            recipe = cur.execute(self.sql_dish_id_count.format(dish_name)).fetchone()
            if recipe[1] == 0:
                return "There is no recipe for this dish."
            recipe_id = recipe[0]
            cur.execute(self.sql_dish_food_delete.format(recipe_id))
            cur.execute(self.sql_dish_delete.format(recipe_id))
            return dish_name + " has been deleted"

    # check which dishes can be cooked with these ingredients
    def check_food(self, ingredients):
        con = sqlite3.connect('test3.db')
        with con:
            cur = con.cursor()
            stock = set(ingredients)
            all_dishes = cur.execute(self.sql_dish_food_all).fetchall()
            result = set()
            for dish in all_dishes:
                dish_food = set(dish[1].split(","))
                if dish_food.issubset(stock):
                    result.add(dish)
            return result

    def list_recipe(self, dish_name):
        con = sqlite3.connect('test3.db')
        with con:
            cur = con.cursor()
            dish_food = cur.execute(self.sql_dish_food_one.format(dish_name)).fetchall()
            return dish_food

    def list_recipes(self):
        con = sqlite3.connect('test3.db')
        with con:
            cur = con.cursor()
            dishes = cur.execute(self.sql_dish_all).fetchall()
            return dishes

    def update_recipe(self, dish_name, ingredients):
        con = sqlite3.connect('test3.db')
        with con:
            cur = con.cursor()
            if cur.execute(self.sql_dish_count.format(dish_name)).fetchall()[0] == 0:
                return "There is no dish '{}'. If you want to add it, please use -a to add.".format(dish_name)
            self.delete_recipe(dish_name)
            self.add_recipe(dish_name, ingredients)
            return "Dish '{}' has been updated.".format(dish_name)


# This function will accept the arguments from the CLI
def main():
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
    print("add", args.add)
    print("delete", args.delete)
    print("read", args.list)
    print("update", args.update)
    print("name", args.name)
    print("check", args.query)
    print("ingredients", args.ingredients)

    obj = SqliteRepository()
    # python3 currentFile.py -a -n KongpoChicken chicken peanut
    # The above will add a recipe "kongpochicken" in table Recipe and ingredients "chicken"
    # and "peanut" in table "Ingredient" and the relation in table Recipe_Ingredient.
    # Note that if the ingredient has been in the table, it would not insert again.
    # If the recipe has been in the table, it would insert nothing and print the prompt.
    if args.add:
        print(obj.add_recipe(args.name.lower(), args.ingredients))
    # python3 currentFile.py -c chicken peanut onion
    # The above will check which dish can be cooked with these ingredients.
    # It would print ('kongpochicken', 'chicken, peanut') like ('dish', 'food1,food2,food3,...').
    elif args.query:
        print(obj.check_food(args.ingredients))
    # python3 currentFile.py -r -n kongpoChicken
    # The above will read the ingredients of this dish
    # It would print ('kongpochicken', 'chicken,peanut') like ('dish', 'food1,food2,food3,...').
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
        print(obj.delete_recipe(args.name.lower()))
    elif args.update:
        print(obj.update_recipe(args.name.lower(), args.ingredients))


if __name__ == "__main__":
    main()
