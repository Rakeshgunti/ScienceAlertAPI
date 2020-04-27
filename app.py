import jwt
import config
import util
from functools import wraps
from models.database import pymongo
from marshmallow import ValidationError
from datetime import datetime, timedelta
from models.validation import RegistrationSchema
from flask import Flask, request, jsonify, make_response, json

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = pymongo(app)

def CheckToken(f):
    @wraps(f)
    def decorator(*args, **kwargs): 
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithm=['HS512'])
            current_user = db.get_user(data['email'], data['_id'])
        except:
            return jsonify({'message': 'token is invalid'})
        return f(current_user, *args, **kwargs)
    return decorator

@app.route("/", methods=["GET"])
@app.route("/api", methods=["GET"])
def home_page():
    return db.get_msg('welcome')

@app.route("/api/register", methods=["POST"])
def register():
    try:
        data = dict(request.get_json())
        if util.Check_all(data.keys(), ['name', 'email', 'password']):
            register = RegistrationSchema().dump(data)
            if not db.get_user(register['email'], None) and db.insert_user(register):
                return db.get_msg('registration')
            else:
                raise ValidationError('User already exists! Please login')
        else:
            raise ValidationError('Data provided should consist of valid name, email, password in JSON format')
    except ValidationError as err:
        return dict(message=err.messages)

@app.route("/api/login", methods=["POST"])
def login():
    try:
        data = dict(request.get_json())
        if util.Check_all(data.keys(), ['email', 'password']):
            user = db.get_user(data['email'], None)
            if util.encrypt(data['password']) == user['password']:
                return jsonify({'token':  util.create_token( user['email'], str(user['_id']), 
                                            app.config['JWT_SECRET_KEY'])})
        raise ValidationError('Invalid username or Password!!')
    except ValidationError as err:
        return dict(message=err.messages)

@app.route("/api/latest", methods=["GET"])
@CheckToken
def get_latest(user):
    return jsonify({'result': db.get_latest()})

@app.route("/api/trending", methods=["GET"])
@CheckToken
def get_trending(user):
    return jsonify({'result' : db.get_trending()})

@app.route("/api/search/date", methods=["GET"])
@CheckToken
def search_date(user):
    try:
        news = 'latest'
        if request.args.get('news'):
            news = request.args.get('news')
        date = util.validate_datepat(request.args.get('query'))
        if news == 'latest':
            return jsonify({'result':db.search_latest_date(date)})
        elif news == 'trending':
            return jsonify({'result':db.search_trending_date(date)})
        else:
            raise ValidationError('Invalid news type. It should be either latest or trending')
    except ValidationError as err:
        return jsonify({'message': err})

@app.route("/api/search/category", methods=["GET"])
@CheckToken
def search_category(user):
    try:
        category_name = request.args.get('query')
        try:
            page = int(request.args.get('page'))
        except ValueError:
            page = 1
        if category_name and page:
            result = db.search_latest_category(category_name.upper(), page)
            return jsonify({'result':result})
        else:
            raise ValidationError('Invalid category or page values. Please check')
    except ValidationError as err:
        return jsonify({'message': err})

@app.route("/api/search/author", methods=["GET"])
@CheckToken
def search_author(user):
    try:
        author_name = request.args.get('query')
        result = db.search_author(author_name.upper())
        return jsonify({'result':result})
    except ValidationError as err:
        return jsonify({'message': err})

if __name__ == "__main__":
    app.run(host='localhost', debug=True, port=5000)