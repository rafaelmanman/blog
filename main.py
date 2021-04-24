from flask import Flask, render_template,request
from post import Post
import sqlite3, os

app = Flask('app')

post0 = {
    'id': 0,
    'title': 'First Post!',
    'body': 'This is my first post'
}

post1 = {
    'id': 1,
    'title': 'First Post With related content',
    'body': 'welcome, this blog has other content as well.'
}

posts = [post0, post1]

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

def entryToPost(entry):
    id = entry[0]
    title = entry[1]
    body = entry[2]
    return Post(id, title, body)

def getAllPosts():
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute('select * from Posts')
    rows = cursor.fetchall()
    db.close()

    posts = [entryToPost(row) for row in rows]

    return posts

def getPostById(post_id):
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute('select * from Posts where id = (?)', (post_id,))
    rows = cursor.fetchall()
    post = entryToPost(rows[0])
    db.close()
    return post

if not os.path.exists('database.db'):
    createDB()

@app.route('/')
def index():
    posts = getAllPosts()
    return render_template("index.html", posts=posts)
    

@app.route("/post/<int:post_id>")
def post(post_id):
    post = getPostById(post_id)
    return render_template('post.html', post=post)

@app.route("/newpost", methods=['GET', 'POST'])
def newpost():
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')
        writePost(title, body)
    return render_template('newpost.html')

app.run(host='0.0.0.0', port='8080')
