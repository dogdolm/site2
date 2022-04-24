from flask import Flask
from flask import render_template
from flask import request
import sqlite3
import hashlib

app = Flask(__name__)
file = open('config', 'r')
passwd = file.read()
file.close()
passwdhash = hashlib.sha256(passwd.encode('UTF-8'))
del passwd



@app.route('/')
def index():
    conn = sqlite3.connect('db.sqlite')
    cur = conn.cursor()
    cur.execute("""select about from main;""")

    for text in cur.fetchone():
        textindex = text
    contextindex = {
        'hello': textindex
    }
    return render_template('index.html', **contextindex)
    conn.close()


@app.route('/blog/')
def blog():
    conn = sqlite3.connect('db.sqlite')
    cur = conn.cursor()
    cur.execute("""select story from blog where visible = TRUE;""")
    stories = list(cur.fetchall())
    cur.execute("""select head from blog where visible =  TRUE;""")
    names = list(cur.fetchall())

    for story in stories[0]:
        text = story
    for name in names[0]:
        nameblog = name
    contextblog1 = {'name1': nameblog,
                    'text1': text}
    for story in stories[1]:
        text = story
    for name in names[1]:
        nameblog = name
    contextblog2 = {'name2': nameblog,
                    'text2': text}
    for story in stories[2]:
        text = story
    for name in names[2]:
        nameblog = name
    contextblog3 = {'name3': nameblog,
                    'text3': text}

    return render_template('blog.html', **contextblog1, **contextblog2, **contextblog3)
    conn.close()


@app.route('/about/')
def about():
    conn = sqlite3.connect('db.sqlite')
    cur = conn.cursor()
    cur.execute('''select address from contacts''')
    for i in cur.fetchone():
        addr = i
        break
    cur.execute('''select phone from contacts''')
    for i in cur.fetchone():
        phone = i
        break
    cur.execute('''select email from contacts''')
    for i in cur.fetchone():
        email = i
        break
    contextabout = {'place': addr, 'phone': phone, 'email': email}
    return render_template('about.html', **contextabout)
    conn.close()


@app.route('/login/', methods=['GET', 'POST'])
@app.route('/login/<int:db_id>/')
def login(db_id=None):
    if request.method == 'POST':
        pas = request.form.get('password')
        pashash = hashlib.sha256(pas.encode('UTF-8'))
        if pashash.hexdigest() != passwdhash.hexdigest():
            return 'Доступ закрыт, попытка взлома'

        db_id = request.form.get('db_id')
        caption = request.form.get('caption')
        author = request.form.get('author')
        visible = True if request.form.get('visible') else False

        conn = sqlite3.connect('db.sqlite')
        cur = conn.cursor()

        cur.execute("""update blog set head = ?, story = ?, visible = ? where id == ?;""",
                    (caption, author, visible, db_id))
        conn.commit()
        conn.close()

        return 'Информация обновлена! <a href="/blog/">Перейти на страницу</a>'

    if db_id is None:
        return "Введите номер истории"

    conn = sqlite3.connect('db.sqlite')
    cur = conn.cursor()

    cur.execute("""select id, head, story, visible from blog where id ==?;""",
                (db_id,))
    context = None

    for db_id, caption, author, visible in cur.fetchall():
        context = {'db_id': db_id, 'caption': caption, 'author': author, 'visible': visible}
    conn.close()

    if context is None:
        return 'Такой книги нет'

    return render_template('form.html', **context)


if __name__ == '__main__':
    app.run()
