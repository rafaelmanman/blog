import sqlite3

def createDB():
    db = sqlite3.connect('database.db')
    db.execute('create table Posts (id integer primary key autoincrement, title text, body text)')
    db.close()

def writePost(title, body):
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute('insert into Posts values (null, ?, ?)', (title, body,))
    db.commit()
    db.close()

def getAllPosts():
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute('select * from Posts')
    rows = cursor.fetchall()
    db.close()
    return rows

def getPostById(post_id):
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute('select * from Posts where id = (?)', (post_id,))
    rows = cursor.fetchall()
    db.close()
    return rows

print(getPostById(1))
