from os.path import join, dirname
from dotenv import load_dotenv
import flask, os
from flask_sqlalchemy import SQLAlchemy
import flask_socketio
import flask_sqlalchemy
import flask_socketio
from flask_socketio import SocketIO, send
import requests

DATA_RECEIVED_CHANNEL = 'data_received_channel'

app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)

sql_user = os.environ['SQL_USER']
sql_pwd = os.environ['SQL_PASSWORD']
dbuser = os.environ['USER']
api_key = os.getenv("API_KEY")

database_uri = os.environ['DATABASE_URL']

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app

import tables
db.session.commit()

def emit_all(channel):
    all_messages = [ \
        db_message.message for db_message \
        in db.session.query(tables.Messages).all()
    ]
        
    all_users = [ \
        db_user.username for db_user \
            in db.session.query(tables.Messages).all()
    ]
            
    socketio.emit(channel, {
        'all_messages': all_messages,
        'all_users' : all_users
    })

URL = 'https://api.funtranslations.com/translate/sith.json?text='
JOKE_URL='http://api.icndb.com/jokes/random'

def sith_api_response(text):
    txt = URL + text
    sith_api_response = requests.get(
        txt,
        headers={'X-FunTranslations-Api-Secret': api_key },
        )
    data = sith_api_response.json()
    return data

def joke_api_respone():
    response = requests.get(JOKE_URL).json()
    joke = response['value']['joke']
    return joke

def botCommandHandler(msg):
    c = msg.split(' ')
    command = c[0]
    data = []

    if command == "!!about":
        message = 'I am fluent in over six million forms of communication, and can readily...  But today, I will translate anything you say to Sith.'
    
    elif command == '!!help':
        message = 'Commands: \n!!about --> About the Chat bot.\n!!help --> See all commands that this bot responds too.\n!!funtranslate <insert text here> --> translates your text to Sith!'
    
    elif command == '!!funtranslate':
        s = msg.split('!!funtranslate ')
        text_to_translate = s[1]
        translated_text = sith_api_response(text_to_translate)
        message = translated_text['contents']['translated']
    
    elif command == '!!joke':
        translated_text = joke_api_respone()
        message = translated_text
    else:
        message = 'I\'m sorry, but I\'m buy and cannot help you : ( ' 
    data = { 'message': message , 'username': 'Sith Bot' }
    db.session.add(tables.Messages(data['username'], (data['message'])))
    db.session.commit()


# models.db.create_all()
#     addresses = [
#         models.Usps("1600 Pennsylvania"),
#         models.Usps("121 W 21st Ave"),
#         models.Usps("NJIT GITC")]

@app.route('/')
def index():
    # tables.db.create_all()
    # db.session.add(tables.Users("greg", "password"))
    # db.session.commit()
    # exists = db.session.query(tables.Users.id).filter_by(username='greg', password='greg').scalar() is not None
    # print(exists)
    return flask.render_template('index.html')

user_counter = 0

@socketio.on('connect')
def on_connect():
    global user_counter
    user_counter += 1
    print('Someone connected!')

@socketio.on('disconnect')
def on_disconnect():
    global user_counter
    user_counter -= 1
    print ('Someone disconnected!')

@socketio.on('new_user')
def newUserHandler(data):
    db.session.add(tables.Users(data['username'], data['password']))
    db.session.commit()
    socketio.emit('new_user_recieved')

@socketio.on('user_status')
def handleUserStatus(data):
    # name = data['username']
    # password = data['password']
    name = db.session.query(tables.Users.id).filter_by(username=data['username']).scalar() is not None
    if name:
        pw = [r[0] for r in tables.Users.query.filter_by(password=data['password']).values('password')]
        if pw[0] != data['password']:
            print('wrong_password')
            socketio.emit('wrong_password', { 'status' : False })
        else:
            print('success')
            socketio.emit('existing_user', {'status' : True , 'username': data['username']})
            db.session.commit()
    else:
        print('new_user')
        newUserHandler(data)
        socketio.emit('existing_user',  { 'status' : True, 'username': data['username']})
    db.session.commit()

@socketio.on('messages')
def getMessages():
    emit_all(DATA_RECEIVED_CHANNEL)

@socketio.on('message')
def handleMessage(msg):
    print(msg)
    data = []
    if msg['message'][0] + msg['message'][0][0] == '!!':
        botCommandHandler(msg['message'])
       
    for key, value in msg.items():
        temp = { key : value }
        data.append(temp)
    
    db.session.add(tables.Messages(msg['username'], (msg['message'])))
    db.session.commit()
    emit_all('msg')

if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
