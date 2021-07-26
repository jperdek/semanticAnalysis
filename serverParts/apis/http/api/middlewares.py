from functools import wraps
from flask import request
from jwt import decode, exceptions
import json
# used from https://developer.okta.com/blog/2019/03/25/build-crud-app-with-python-flask-angular
import asyncio
from okta_jwt_verifier import JWTVerifier

loop = asyncio.get_event_loop()


def is_access_token_valid(token, issuer='https://dev-03853854.okta.com', client_id = 'gfhjkfdfg can vary'):
    jwt_verifier = JWTVerifier(issuer, client_id, '0oa19wfjhrBoVLqSw5d7')
    try:
        loop.run_until_complete(jwt_verifier.verify_access_token(token))
        return True
    except Exception as e:
        print(e)
        return False


def login_required(f):

    @wraps(f)
    def wrap(*args, **kwargs):
        authorization = request.headers.get("authorization", None)

        if not authorization:
            print("Not authorized")
            return json.dumps({'error': 'no authorization token provided'}), 401, {'Content-type': 'application/json'}
        try:
            token = authorization.split(' ')[1]

            # comment this for deployment
            if token == 'debug':
                print("Debugging request: please comment it for deployment!")
                return f(*args, **kwargs)

            valid = is_access_token_valid(token)
            if not valid:
                return json.dumps({'error': 'invalid authorization token'}), 401, {'Content-type': 'application/json'}
        except exceptions.DecodeError:
            return json.dumps({'error': 'invalid authorization token'}), 401, {'Content-type': 'application/json'}

        return f(*args, **kwargs)
    return wrap