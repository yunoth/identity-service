from app import app
from flaskext.mysql import MySQL

#Create an instance of MySQL
mysql = MySQL()

#Set database credentials in config.
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'identitydb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

#Initialize the MySQL extension
mysql.init_app(app)