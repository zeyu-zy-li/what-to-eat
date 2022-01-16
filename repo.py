import argparse
import sqlite3


class SqliteRepository:
    sql_create_tables_script = "Create Table IF NOT EXISTS Recipe (ID INTEGER PRIMARY KEY AUTOINCREMENT, dish varchar not null);" \
                               + " Create Table IF NOT EXISTS Ingredient (ID INTEGER PRIMARY KEY AUTOINCREMENT, food varchar not null);" \
                               + " Create Table IF NOT EXISTS Recipe_Ingredient (ID INTEGER PRIMARY KEY AUTOINCREMENT, Recipe_ID INTEGER, Ingredient_ID INTEGER, Foreign Key (Recipe_ID) REFERENCES Recipe(ID), Foreign KEY (Ingredient_ID) REFERENCES Ingredient(ID));"
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

    def __init__(self, db_name):
        self.con = sqlite3.connect(db_name)
        with self.con:
            cur = self.con.cursor()
            cur.executescript(self.sql_create_tables_script)

    # add recipe with the "dishName" and [ingredients]
    def add_recipe(self, dish_name, ingredients):
        with self.con:
            cur = self.con.cursor()
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

    # delete the recipe with the name of "dishName"
    def delete_recipe(self, dish_name):
        with self.con:
            cur = self.con.cursor()
            recipe = cur.execute(self.sql_dish_id_count.format(dish_name)).fetchone()
            if recipe[1] == 0:
                return "There is no recipe for this dish."
            recipe_id = recipe[0]
            cur.execute(self.sql_dish_food_delete.format(recipe_id))
            cur.execute(self.sql_dish_delete.format(recipe_id))
            return dish_name + " has been deleted"

    # check which dishes can be cooked with these ingredients
    def check_food(self, ingredients):
        with self.con:
            cur = self.con.cursor()
            stock = set(ingredients)
            all_dishes = cur.execute(self.sql_dish_food_all).fetchall()
            result = set()
            for dish in all_dishes:
                dish_food = set(dish[1].split(","))
                if dish_food.issubset(stock):
                    result.add(dish)
            return result

    def list_recipe(self, dish_name):
        with self.con:
            cur = self.con.cursor()
            dish_food = cur.execute(self.sql_dish_food_one.format(dish_name)).fetchall()
            return dish_food

    def list_recipes(self):
        with self.con:
            cur = self.con.cursor()
            dishes = cur.execute(self.sql_dish_all).fetchall()
            return dishes

    def update_recipe(self, dish_name, ingredients):
        with self.con:
            cur = self.con.cursor()
            if cur.execute(self.sql_dish_count.format(dish_name)).fetchall()[0] == 0:
                return "There is no dish '{}'. If you want to add it, please use -a to add.".format(dish_name)
            self.delete_recipe(dish_name)
            self.add_recipe(dish_name, ingredients)
            return "Dish '{}' has been updated.".format(dish_name)


