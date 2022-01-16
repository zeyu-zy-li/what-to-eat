from repo import *
import pytest


@pytest.fixture
def empty_db():
    repo = SqliteRepository(':memory:')
    with repo.con as con:
        cur = con.cursor()
        cur.executescript(SqliteRepository.sql_create_tables_script)
    return repo


@pytest.fixture
def db_with_data(empty_db):
    con = empty_db.con
    with con:
        cur = con.cursor()
        cur.execute(SqliteRepository.sql_dish_insert.format('kongpochicken'))
        cur.execute(SqliteRepository.sql_food_insert.format('chicken'))
        cur.execute(SqliteRepository.sql_food_insert.format('peanut'))
        dish1_id = cur.execute(SqliteRepository.sql_dish_id.format('kongpochicken')).fetchone()[0]
        food1_id, = cur.execute(SqliteRepository.sql_food_id.format('chicken')).fetchone()
        food2_id, = cur.execute(SqliteRepository.sql_food_id.format('peanut')).fetchone()
        cur.execute(SqliteRepository.sql_dish_food_insert.format(dish1_id, food1_id))
        cur.execute(SqliteRepository.sql_dish_food_insert.format(dish1_id, food2_id))
    return empty_db


# tests for function addRecipe
def test_add_recipe(empty_db):
    target_dish = 'kongpochicken'
    target_ingredients = ['chicken', 'peanut']
    empty_db.add_recipe(target_dish, target_ingredients)
    con = empty_db.con
    with con:
        cur = con.cursor()
        sql_dish_food_one = "SELECT dish, group_concat(food) FROM Recipe JOIN Recipe_Ingredient ON Recipe.ID = Recipe_Ingredient.Recipe_ID JOIN Ingredient ON Recipe_Ingredient.Ingredient_ID = Ingredient.ID WHERE dish = '{}' GROUP BY dish;"
        dish_name, ingredients = cur.execute(sql_dish_food_one.format(target_dish)).fetchone()
    assert dish_name == target_dish
    assert set(ingredients.split(',')) == set(target_ingredients)


def test_add_recipe_again(db_with_data):
    try:
        target_dish = 'kongpochicken'
        target_ingredients = ['chicken', 'peanut']
        db_with_data.add_recipe(target_dish, target_ingredients)
    except DishExistsError:
        assert True
    finally:
        con = db_with_data.con
        with con:
            cur = con.cursor()
            num_same_dish, = cur.execute(SqliteRepository.sql_dish_count.format('kongpochicken')).fetchone()
        assert num_same_dish == 1


def test_add_same_food(db_with_data):
    target_dish = 'currychicken'
    target_ingredients = ['chicken', 'potato']
    db_with_data.add_recipe(target_dish, target_ingredients)
    con = db_with_data.con
    with con:
        cur = con.cursor()
        num_same_food, = cur.execute(SqliteRepository.sql_food_count.format('chicken')).fetchone()
    assert num_same_food == 1


def test_delete_no_recipe(db_with_data):
    try:
        target_dish = 'currychicken'
        db_with_data.delete_recipe(target_dish)
    except DishNotExistsError:
        assert True


def test_delete_recipe(db_with_data):
    target_dish = 'kongpochicken'
    con = db_with_data.con
    with con:
        cur = con.cursor()
        dish_id, = cur.execute(SqliteRepository.sql_dish_id.format(target_dish)).fetchone()
        db_with_data.delete_recipe(target_dish)
        num_dish, = cur.execute(SqliteRepository.sql_dish_count.format(target_dish)).fetchone()
        num_dish_food, = cur.execute(
            "SELECT COUNT(ID) FROM Recipe_Ingredient WHERE Recipe_ID = {};".format(dish_id)).fetchone()
    assert num_dish == 0
    assert num_dish_food == 0


def test_update_no_recipe(db_with_data):
    try:
        target_dish = 'currychicken'
        target_ingredients = ['chicken', 'carrot']
        db_with_data.update_recipe(target_dish, target_ingredients)
    except DishNotExistsError:
        assert True


def test_update_recipe(db_with_data):
    target_dish = 'kongpochicken'
    target_ingredients = ['chicken', 'onion', 'carrot']
    db_with_data.update_recipe(target_dish, target_ingredients)
    con = db_with_data.con
    with con:
        cur = con.cursor()
        dish, ingredients = cur.execute(SqliteRepository.sql_dish_food_one.format(target_dish)).fetchone()
    assert dish == target_dish
    assert set(ingredients.split(',')) == set(target_ingredients)
