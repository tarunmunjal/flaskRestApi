from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
from flaskext.mysql import MySQL
from flask import Response
import json
app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'changeme'
app.config['MYSQL_DATABASE_PASSWORD'] = 'changeme'
app.config['MYSQL_DATABASE_DB'] = 'changeme'
app.config['MYSQL_DATABASE_HOST'] = 'changeme'


mysql.init_app(app)

api = Api(app)

class CreateUser(Resource):
    def post(self):
        try:
            #Parse the arguments using reqparser
            parser = reqparse.RequestParser()
            parser.add_argument('email',type=str, help='Email address to create user')
            parser.add_argument('password',type=str, help='Password to create user')
            args = parser.parse_args()
            _userEmail = args['email']
            _userPassword = args['password']
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('spCreateUser',(_userEmail,_userPassword))
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                return {'StatusCode':'200','Message': 'User creation success'}
            else:
                return {'error':'500','Message': str(data[0])}
        except Exception as e:
            return{'error': str(e)}

api.add_resource(CreateUser,'/CreateUser')

@app.route("/users")
def listAllUsers():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select * from ItemListDb.tblUser")
    queryResult = [ dict(line) for line in [zip([ column[0] for column in cursor.description], row) for row in cursor.fetchall()] ]
    return json.dumps(queryResult)

@app.route("/testuser", methods=['GET'])
def testUser():
    return json.dumps({ "name":"John", "age":30, "car":"Labmorgini" }) 

if __name__ == '__main__':
    app.run(port=80)