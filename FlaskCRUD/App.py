# from flask import Flask, render_template, request, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crud.db'  # SQLite database file
# db = SQLAlchemy(app)
#
# class Task(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#
# @app.route('/')
# def index():
#     tasks = Task.query.all()
#     return render_template('index.html', tasks=tasks)
#
# @app.route('/add', methods=['POST'])
# def add():
#     title = request.form.get('title')
#     new_task = Task(title=title)
#     db.session.add(new_task)
#     db.session.commit()
#     return redirect(url_for('index'))
#
# @app.route('/delete/<int:id>')
# def delete(id):
#     task_to_delete = Task.query.get(id)
#     db.session.delete(task_to_delete)
#     db.session.commit()
#     return redirect(url_for('index'))
#
# if __name__ == '__main__':
#     db.create_all()  # Create database tables
#     app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crudemployee'

mysql = MySQL(app)

@app.route('/')
def index():
    curs = mysql.connection.cursor()
    curs.execute("SELECT * FROM employees")
    data = curs.fetchall()
    curs.close()

    return render_template('index.html', employees = data)

@app.route('/add', methods = ['POST'])
def add():
    if request.method == "POST":
        name = request.form['name']
        address = request.form['address']
        phone = request.form['phone']
        email = request.form['email']

        curs = mysql.connection.cursor()
        curs.execute("INSERT INTO employees (name, address, phone, email) VALUES (%s, %s, %s, %s)", (name, address, phone, email))
        mysql.connection.commit()
        return redirect(url_for('index'))

@app.route('/edit', methods = ['POST', 'GET'])
def edit():
    if request.method == "POST":
        data_id = request.form['id']
        name = request.form['name']
        address = request.form['address']
        phone = request.form['phone']
        email = request.form['email']

        curs = mysql.connection.cursor()
        curs.execute("UPDATE employees SET name=%s, address=%s, phone=%s, email=%s WHERE id=%s ",
                     (name, address, phone, email, data_id))
        mysql.connection.commit()
        return redirect(url_for('index'))

@app.route('/delete/<string:data_id>', methods = ['POST', 'GET'])
def delete(data_id):
        curs = mysql.connection.cursor()
        curs.execute("DELETE FROM employees WHERE id = %s", (data_id))
        mysql.connection.commit()
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)