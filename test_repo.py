from repo import SqliteRepository


# tests for function addRecipe
def test_add_recipe():
    repo = SqliteRepository(':memory:')
    target_dish = 'kongpo'
    target_ingredients = ['chicken', 'carrot']
    result = repo.add_recipe(target_dish, target_ingredients)
    con = repo.con
    cur = con.cursor()
    sql_dish_food_one = "SELECT dish, group_concat(food) FROM Recipe JOIN Recipe_Ingredient ON Recipe.ID = Recipe_Ingredient.Recipe_ID JOIN Ingredient ON Recipe_Ingredient.Ingredient_ID = Ingredient.ID WHERE dish = '{}' GROUP BY dish;"
    dish_name, ingredients = cur.execute(sql_dish_food_one.format(target_dish)).fetchone()
    assert result == "This dish is added successfully."
    assert dish_name == target_dish
    assert set(ingredients.split(',')) == set(target_ingredients)



        
        