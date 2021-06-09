#import os
import jwt
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta


class Auth:
    hasher = CryptContext(schemes=['bcrypt'])
    #secret = os.getenv("SECRET_KEY")
    secret = 'kAkCE~DrHB"mTKTy"uQwgdk1qj|!|I:}T~5UtVTbI`IxVnY.G}VJkAwj6H#Anv&' # Simon will fix this up later on

    def encode_password(self,password):
        return self.hasher.hash(password)

    def verify_password(self, password, encoded_password):
        return self.hasher.verify(password, encoded_password)

    def encode_token(self, username):
        payload = {
            'exp' : datetime.utcnow()+timedelta(days=0, minutes=30),
            'iat' : datetime.utcnow(),
            'scope' : 'access_token',
            'sub' : username
        }
        return jwt.encode(payload,self.secret,algorithm='HS256')

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            if payload['scope'] == 'access_token':
                return payload['sub']
            raise HTTPException(status_code=401, detail='Invalid token scope')
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Token expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')

    def encode_refresh_token(self, username):
        payload = {
            'exp' : datetime.utcnow() + timedelta(days=0, hours=10),
            'iat' : datetime.utcnow(),
        'scope': 'refresh_token',
            'sub' : username
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )

    def refresh_token(self, refresh_token):
        try:
            payload = jwt.decode(refresh_token, self.secret, algorithms=['HS256'])
            if payload['scope'] == 'refresh_token':
                username = payload['sub']
                new_token = self.encode_token(username)
                return new_token
            raise HTTPException(status_code=401, detail='Invalid token scope')
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Token expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')

