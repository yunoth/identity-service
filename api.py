import pymysql
from config import mysql
from app import app
from flask import Flask, jsonify, request, session

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

@app.route('/login', methods=['POST'])
def login():
    conn = None
    cursor = None
    try:
        json = request.json
        username = json['username']
        password = json['password']

        # validate the received values
        if username and password:
            #check user exists
            conn = mysql.connect()
            cursor = conn.cursor()
            sql = "SELECT * FROM users WHERE username=%s"
            data = (username)
            cursor.execute(sql, data)
            row = cursor.fetchone()
            if row:
                if row[2] == password:
                    #session['username'] = row[1]
                    return jsonify({'message': 'You are logged in successfully'})
                else:
                    resp = jsonify({'message': 'Bad Request - invalid password'})
                    resp.status_code = 400
                    return resp
        else:
            resp = jsonify({'message': 'Bad Request - invalid credendtials'})
            resp.status_code = 400
            return resp
    except:
        resp = jsonify({'message':'invalid request'})
        resp.status_code = 400
        return resp
    finally:
        if cursor and conn:
            cursor.close()
            conn.close()

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username', None)
    return jsonify({'message' : 'You successfully logged out'})

@app.route('/')
def home():
    if 'username' in session:
        #username = session['username']
        return jsonify({'message' : 'You are already logged in', 'username' : username})
    else:
        resp = jsonify({'message' : 'Unauthorized'})
        resp.status_code = 401
        return resp

if __name__ == "__main__":
    app.run(debug=True, use_debugger=True)