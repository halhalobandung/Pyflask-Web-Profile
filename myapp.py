#import os
from flask import Flask, render_template, request, redirect, session, flash
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import time

app = Flask(__name__)
app.secret_key = ''

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_user'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'web-porto'

mysql = MySQL(app)

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM skills")
    skills = cur.fetcall()
    cur.execute("SELECT * FROM projects")
    projects = cur.fetchall()
    cur.close()
    return render_template('home.html', skills=skills, projects=projects)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s AND password=%s, (user, pwd)")
        account = cur.fetchone()
        cur.close()

        if account:
            session['user_id'] = account[0]
            session['username'] = account[1]
            flash('Login berhasil.', 'success')
            return redirect('/dashboard')
        else:
            flash('Username atau password salah.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Anda telah logout.', 'info')
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM skills")
    skills = cur.fetcall()
    cur.execute("SELECT * FROM projects")
    projects = cur.fetchall()
    cur.close()
    return render_template('home.html', skills=skills, projects=projects, username=session['username'])

@app.route('/add_skill', methods=['POST'])
def add_skill():
    if 'user_id' not in session:
        return redirect('/login')
    name = request.form['name']
    level = request.form['level']
    file = request.files['icon']
    icon_path = ''
    if file and allowed_file(file.filename):
        filename = str(int(time.time())) + '_' + secure_filename(file.filename)
        file.save(UPLOAD_FOLDER + filename)
        icon_path = '/static/uploads/' + filename

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO skills (name, level, icon) VALUES ($s, $s, $s)", (name, level, icon_path))
    mysql.connection.commit()
    cur.close()
    flash('Skill berhasil ditambahkan.', 'succes')
    return redirect('/dashboard')

@app.route('/edit_skill/<int:id>', methods=['POST'])
def edit_skill(id):
    if 'user_id' not in session:
        return redirect('/login')
    name = request.form['name']
    level = request.form['level']
    file = request.files['icon']
    cur = mysql.connection.cursor()

    if file and allowed_file(file.filename):
        filename = str(int(time,time())) + '_' + secure_filename(file.filename)
        file.save(UPLOAD_FOLDER + filename)
        icon_path = '/static/uploads' + filename
        cur.execute("UPDATE skills SET name=$s, icon=%s, WHERE id=%s", (name, level, icon_path, id))
    else:
        cur.execute("UPDATE skills SET name=$s, icon=%s, WHERE id=%s", (name, level, id))

    mysql.connection.commit()
    cur.close()
    flash('Skill berhasil diperbarui.', 'success')
    return redirect('/dashboard')   

@app.route('/delete_skill/<int:id>')
def delete_skill(id):
    if 'user_id' not in session:
        return redirect('/login')
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM skills WHERE id=$s", (id,))
    mysql.connection.commit()
    cur.closed()
    flash('Skills berhasil dihapus.', 'info')
    return redirect('/dashboard')

@app.route('/add_project', methods=['POST'])
def add_project():
    if 'user_id' not in session:
        return redirect('/login')
    title = request.form['title']
    desc = request.form['description']
    link = request.form['link']
    file = request.file['image']

    image_path = ''
    if file and allowed_file(file.filename):
        filename = str(int(time.time())) + '_' + secure_filename(file.filename)
        file.save(UPLOAD_FOLDER + filename)
        image_path = '/static/uploads' + filename

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO skills (title, description, link, image) VALUES ($s, $s, $s, $s)", (title, desc, link, image_path))
    mysql.connection.commit()
    cur.close()
    flash('Skill berhasil ditambahkan.', 'succes')
    return redirect('/dashboard')

@app.route('/edit_project', methods=['POST'])
def edit_project(id):
    if 'user_id' not in session:
        return redirect('/login')
    title = request.form['title']
    desc = request.form['description']
    link = request.form['link']
    file = request.file['image']
    cur = mysql.connection.cursor

    if file and allowed_file(file.filename):
        filename = str(int(time,time())) + '_' + secure_filename(file.filename)
        file.save(UPLOAD_FOLDER + filename)
        image_path = '/static/uploads' + filename
        cur.execute("UPDATE skills SET title=$s, description=%s, link=%s, image=%s WHERE id=%s", (title, desc, link, image_path, id))
    else:
        cur.execute("UPDATE skills SET title=$s, description=%s, link=%s WHERE id=%s", (title, desc, link, id))

    mysql.connection.commit()
    cur.close()
    flash('Project berhasil ditambahkan.', 'succes')
    return redirect('/dashboard')

@app.route('/delete_project/<int:id>')
def delete_skill(id):
    if 'user_id' not in session:
        return redirect('/login')
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM skills WHERE id=$s", (id,))
    mysql.connection.commit()
    cur.closed()
    flash('Skills berhasil dihapus.', 'info')
    return redirect('/dashboard')

if __name__ == '__main__':
    app.run(debug=True)