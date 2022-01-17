# what-to-eat

## Introduction

This project is used to restore the recipes of dishes and help to decide what to eat with the current ingredients.

It is a *CLI* project using **SQLite3** as the database with python3 as the programming language.

It can be used with `cli.py`, `repo.py` in local PC with `test_repo.py` as the unittest using pytest.

It also works with `server.py` working as server using flask, `cli_client.py` working as client using requests.

## How to use

### local


#### cmd

```
python3 cli.py -l # list all the dish names in database

python3 cli.py -l -n <dish_name> # list all the ingredients of this dish

python3 cli.py -a -n <dish_name> <food1> <food2> ... # add a recipe with the dish name and ingredients

python3 cli.py -u -n <dish_name> <food1> <food2> ... # update the ingredients of this dish

python3 cli.py -d -n <dish_name> # delete the recipe with the dish name

python3 cli.py -q <food1> <food2> ... # check "what to eat", list all the dishes and their ingredients which can be cooked with the current food stock
```

### client-server

#### server

install flask

```
export FLASK_APP = server

flask run #running on http://127.0.0.1:5000
```

#### client

install requests

The same with the local above except replacing `cli.py` into `cli_client.py`.
