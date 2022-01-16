from flask import Flask
from flask import request, jsonify, Response
from repo import *

app = Flask("server")


# get /recipes         //-l
@app.route('/recipes')
def list_all_recipes():
    repo = SqliteRepository('recipe.db')
    return jsonify(repo.list_recipes())


# post /recipes       //-a -n xx xxxx payload
@app.route('/recipes', methods=['POST'])
def create_recipe():
    repo = SqliteRepository('recipe.db')
    data = request.get_json()
    try:
        repo.add_recipe(data['dish'], data['ingredients'])
    except DishExistsError as e:
        return Response(str(e), status=409)
    return Response("Successfully added!")


# get /recipe/dish     //-l -n xx
@app.route("/recipe/<dish_name>")
def list_one_recipe(dish_name):
    repo = SqliteRepository('recipe.db')
    return jsonify(repo.list_recipe(dish_name))


# put /recipe/dish     //-u -n xx
@app.route("/recipe/<dish_name>", methods=['PUT'])
def upgrade_recipe(dish_name):
    repo = SqliteRepository('recipe.db')
    data = request.get_json()
    try:
        repo.update_recipe(dish_name, data['ingredients'])
    except DishNotExistsError as e:
        return Response(str(e), status=404)
    return Response("{} has been updated".format(dish_name))


# delete /recipe/dish   //-d -n xx
@app.route("/recipe/<dish_name>", methods=['DELETE'])
def delete_recipe(dish_name):
    repo = SqliteRepository('recipe.db')
    try:
        repo.delete_recipe(dish_name)
    except DishNotExistsError as e:
        return Response(e.__str__(), status=404)
    return Response("{} has been deleted.".format(dish_name))


# post /recipes/check    //-q xxxx payload
@app.route("/recipes/check", methods=['POST'])
def check_recipe():
    repo = SqliteRepository('recipe.db')
    data = request.get_json()
    return Response(str(repo.check_food(data['ingredients'])))
