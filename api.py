import pymysql
from config import mysql
from app import app
from flask import Flask, jsonify, request

# CRUD Operation - CREATE
@app.route('/add', methods=['POST'])
def add():
    try:
        json = request.json
        username = json['username']
        email = json['email']
        password = json['password']
        if username and email and password and request.method == 'POST':
             SQL_Query = "INSERT INTO users(username, email, password, lastlogin) VALUES(%s, %s, %s, current_timestamp())"
             data = (username, email, password,)
             connection = mysql.connect()
             Pointer = connection.cursor()
             Pointer.execute(SQL_Query, data)
             connection.commit()
             response = jsonify('user added successfully!')
             response.status_code = 200
             return response
        else:
             return jsonify('invalid data')
    except:
        return jsonify('invalid request')
    finally:
        Pointer.close()
        connection.close()

#CRUD Operation - DELETE
@app.route('/delete/<string:id>', methods=['POST'])
def delete(id):
    try:
        connection = mysql.connect()
        Pointer = connection.cursor()
        Pointer.execute("DELETE FROM users WHERE username=%s", (id,))
        connection.commit()
        response = jsonify('user deleted!')
        response.status_code = 200
        return response
    except:
        return jsonify('invalid request')
    finally:
        Pointer.close()
        connection.close()

#CRUD Operation - READ
@app.route('/list/<string:username>', methods=['POST'])
def list(username):
    try:
        connection = mysql.connect()
        Pointer = connection.cursor(pymysql.cursors.DictCursor)
        Pointer.execute("SELECT * FROM users WHERE username=%s", username)
        record = Pointer.fetchone()
        response = jsonify(record)
        response.status_code = 200
        return response
    except:
        return jsonify('invalid request')
    finally:
        Pointer.close()
        connection.close()

@app.route('/listall', methods=['GET'])
def listall():
    try:
        connection = mysql.connect()
        Pointer = connection.cursor(pymysql.cursors.DictCursor)
        Pointer.execute("SELECT * FROM users")
        record = Pointer.fetchall()
        response = jsonify(record)
        response.status_code = 200
        return response
    except:
        return jsonify('invalid request')
    finally:
        Pointer.close()
        connection.close()

#CRUD Operation - UPDATE
@app.route('/update', methods=['POST'])
def update():
    try:
        json = request.json
        username = json['username']
        password = json['password']
        email = json['email']
        if username and password and email and request.method == 'POST':
            SQL_Query = "UPDATE users SET password=%s, email=%s WHERE username=%s"
            data = (password, email, username)
            connection = mysql.connect()
            Pointer = connection.cursor()
            Pointer.execute(SQL_Query, data)
            connection.commit()
            response = jsonify('user details updated')
            response.status_code = 200
            return response
        else:
            return 'not_found'
    except:
        return jsonify('invalid request')
    finally:
        Pointer.close()
        connection.close()



if __name__ == "__main__":
    app.run(debug=True, use_debugger=True)