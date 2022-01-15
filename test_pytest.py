from stock1 import *
# tests for function addRecipe
def test_addRecipe_newDish_newFood():
    con = sqlite3.connect('test3.db')
    with con:
        cur = con.cursor()
        
        