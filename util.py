import jwt
import hashlib
from marshmallow import ValidationError
from datetime import datetime, timedelta

def encrypt(data):
    return hashlib.sha512(data.encode()).hexdigest()

def Check_all(data, li):
    return all([(i in data) for i in li])

def create_token(email, _id, secret_key):
    payload = {
            'email':email, 
            '_id': _id, 
            '_time': str(datetime.utcnow()),
            'exp': datetime.utcnow() + timedelta(hours=1)}
    return jwt.encode(payload, secret_key, algorithm='HS512').decode('UTF-8')

def validate_datepat(date):
    if '-' in date:
        return datetime.strptime(date,"%Y-%m-%d")
    elif '/' in date:
        return datetime.strptime(date,"%Y/%m/%d")
    else:
        raise ValidationError('Invalid date pattern. Date should be like yyyy-mm-dd or yyyy/mm/dd')