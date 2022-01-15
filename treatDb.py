import sqlite3
import sys

con = sqlite3.connect('test.db')
with con:
    cur = con.cursor()
    data1 = cur.execute('select * from Recipe').fetchall()
    data2 = cur.execute('select food from Ingredient').fetchall()
    data3 = cur.execute('select dish from Recipe join Ingredient on Recipe.ID = Ingredient.dish_id').fetchmany()
    # print(data2)
    # print('potato' in data2)
    # print(data3)

    # print(('potato',) in cur.execute('select food from Ingredient where food = "potato"').fetchmany())
    # print('potato' in cur.execute('select food from Ingredient where food = "potato"'))

    # cur.execute('create table t(ID INTEGER PRIMARY KEY AUTOINCREMENT, name varchar)')
    # cur.execute("Insert into t(name) values('aaa')")
    # print(cur.execute('select * from t').fetchall())
    # data4 = cur.execute("Select dish, group_concat(food) from Recipe join Recipe_Ingredient on Recipe.ID = Recipe_Ingredient.Recipe_ID join Ingredient on Recipe_Ingredient.Ingredient_ID = Ingredient.ID group by dish;").fetchall()
    # ingre_set = set(data4[1][1].split(","))
    # print(set(data4[1][1].split(",")))
    # check = {'onion','potato'}.issubset(ingre_set)
    # print(check)
    data5 = cur.execute("select ID, count(ID) from Recipe where dish = 'aaa';").fetchone()
    print(data5)
    # for dish in data4:
    #     dish[1]