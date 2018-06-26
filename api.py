import argparse, os
from flask import Flask, request, Response, json
from flask_restful import Resource, Api, reqparse
from flaskext.mysql import MySQL

#__parserParams = argparse.ArgumentParser(description="RestApi")
#__parserParams.add_argument('--port','-p',help='Port to run the application on',required=True)
#__parserParams.add_argument('--dbserver','-dbs',help='Database Server IP/hostname',required=True)
#__parserParams.add_argument('--dbuser','-dbu',help='Database user',required=True)
#__parserParams.add_argument('--dbpassword','-dbp',help='Database password',required=True)
#__parserParams.add_argument('--dbname','-dbn',help='Database to connect to',required=True)

#__allParameters = __parserParams.parse_args()
#__applicationPort = __allParameters.port
#if os.environ['env_port'] and os.environ['env_dbuser'] and os.environ['env_dbpassword'] and os.environ['env_dbname'] and os.environ['env_dbserver']:
#    print('envfound')
#else:
#    raise Exception('port,dbuser,dbpassword,dbname,dbserver are required params')    
__applicationPort = int(os.environ['env_port'])
app = Flask(__name__)
mysql = MySQL()
######## Database variables
#app.config['MYSQL_DATABASE_USER'] = __allParameters.dbuser
#app.config['MYSQL_DATABASE_PASSWORD'] = __allParameters.dbpassword
#app.config['MYSQL_DATABASE_DB'] = __allParameters.dbname
#app.config['MYSQL_DATABASE_HOST'] = __allParameters.dbserver

app.config['MYSQL_DATABASE_USER'] = os.environ['env_dbuser']
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ['env_dbpassword']
app.config['MYSQL_DATABASE_DB'] = os.environ['env_dbname']
app.config['MYSQL_DATABASE_HOST'] = os.environ['env_dbserver']

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
                return {'status_code':'200','Message': 'User creation success'}
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

@app.route("/createnewusers",  methods=['POST'])
def createnewusers():
    _createnewuseremail = request.json['email']
    _createnewuserpassword = request.json['password']
    email = request.json['email']
    password = request.json['password']
    conn = mysql.connect()
    cursor = conn.cursor()
    querystring = "INSERT INTO ItemListDb.tblUser(UserName,Password) VALUES('%s', '%s');" % (email, password)
    cursor.execute(querystring)
    conn.commit()
    #queryResult = [ dict(line) for line in [zip([ column[0] for column in cursor.description], row) for row in cursor.fetchall()] ]
    queryResult = cursor.fetchall()
    return json.dumps({'results':queryResult})
    #return json.dumps({'results':querystring})

@app.route("/DeleteUser",  methods=['DELETE'])
def deleteuser():
    try:
        email = request.json['email']
        password = request.json['password']
        if not email:
            raise Exception('email parameter is mandatory') 
        if not password:
            raise Exception('password parameter is mandatory')
        conn = mysql.connect()
        cursor = conn.cursor()
        deleteQuery = "DELETE FROM ItemListDb.tblUser WHERE UserName = '%s' AND Password = '%s';" % (email, password)
        cursor.execute(deleteQuery)
        #queryResult = [ dict(line) for line in [zip([ column[0] for column in cursor.description], row) for row in cursor.fetchall()] ]
        conn.commit()
        return json.dumps({'status_code':'200','Message': 'User creation success'})
        #return json.dumps({'querystring':deleteQuery})
    except Exception as e:
        return json.dumps({'status_code':'500','Message': e})

@app.route("/testuser", methods=['GET'])
def testUser():
    return json.dumps({ "name":"John", "age":30, "car":"Labmorgini" }) 

@app.route("/testuser2", methods=['POST'])
def testUser2():
    parser = reqparse.RequestParser()
    parser.add_argument('email')
    parser.add_argument('name')
    parser.add_argument('password')
    args = parser.parse_args()
    return json.dumps({ "name": args }) 


@app.route("/testuser/<string:name>", methods=['GET'])
def testuserselectname(name):
    conn = mysql.connect()
    cursor = conn.cursor()
    #__username = name
    querystring = "select * from ItemListDb.tblUser where UserName like '%{name}%'"
    cursor.execute(querystring)
    queryResult = [ dict(line) for line in [zip([ column[0] for column in cursor.description], row) for row in cursor.fetchall()] ]
    #return json.dumps({'query':querystring})
    return json.dumps(queryResult)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=__applicationPort)