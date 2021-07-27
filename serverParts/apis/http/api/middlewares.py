from functools import wraps
from flask import request
from jwt import decode, exceptions
import jwt
# for new auth verification
# from https://community.auth0.com/t/i-getting-expecting-a-pem-formatted-key/52055/5
from jose import jwt
import json
from six.moves.urllib.request import urlopen
from os import environ as env
from dotenv import load_dotenv, find_dotenv


# THROWS ERROR NOT USED ANY MORE
def is_access_token_valid1(token, issuer='https://dev-03853854.okta.com', client_id='perdek.jakub@gmail.com'):
    # used from https://developer.okta.com/blog/2019/03/25/build-crud-app-with-python-flask-angular
    import asyncio
    from okta_jwt_verifier import JWTVerifier
    jwt_verifier = JWTVerifier(issuer, client_id, '0oa19wfjhrBoVLqSw5d7')
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(jwt_verifier.verify_access_token(token))
        return True
    except Exception as e:
        print(e)
        return False


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
AUTH0_DOMAIN = env.get("dev-03853854.okta.com")
PATH_TO_AUTH_SERVER = "https://dev-03853854.okta.com/oauth2/default/.well-known/oauth-authorization-server"
API_IDENTIFIER = env.get('0oa19wfjhrBoVLqSw5d7')
ALGORITHMS = ["RS256"]


# Format error response and append status code.
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header(raw_token):
    """Obtains the access token from the Authorization Header
    """
    auth = raw_token
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                        "description":
                            "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must start with"
                            " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                        "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must be"
                            " Bearer token"}, 401)

    token = parts[1]
    return token


def decode(auth_header):
    token = get_token_auth_header(auth_header)
    # loads json with all endpoints for auth server
    jsonurl = urlopen(PATH_TO_AUTH_SERVER)
    links = json.loads(jsonurl.read())
    # takes jwks one with json values for auth
    jwks = json.loads(urlopen(links['jwks_uri']).read())

    try:
        unverified_header = jwt.get_unverified_header(token)
    except jwt.JWTError:
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Invalid header. "
                            "Use an RS256 signed JWT Access Token"}, 401)
    if unverified_header["alg"] == "HS256":
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Invalid header. "
                            "Use an RS256 signed JWT Access Token"}, 401)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_IDENTIFIER,
                issuer="https://"+AUTH0_DOMAIN+"/"
            )
        except jwt.ExpiredSignatureError:
            raise AuthError({"code": "token_expired",
                            "description": "token is expired"}, 401)
        except jwt.JWTClaimsError:
            raise AuthError({"code": "invalid_claims",
                            "description":
                                "incorrect claims,"
                                " please check the audience and issuer"}, 401)
        except Exception:
            raise AuthError({"code": "invalid_header",
                            "description":
                                "Unable to parse authentication"
                                " token."}, 401)

        print(payload)


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

            decode(authorization)

        except exceptions.DecodeError as a:
            return json.dumps({'error': 'invalid authorization token'}), 401, {'Content-type': 'application/json'}

        return f(*args, **kwargs)
    return wrap
