from functools import wraps
import requests
import json
from jose import jwt
from flask import request, g
from anonfiles.errors.handle_all import Halt
from config.config import Config


def get_rsa(webkeys, unver):
    """ find matching key and collect key information """
    if unver["alg"] != "RS256":
        raise Halt(1011, "incorrect algorithm")

    for key in webkeys["keys"]:
        if key["kid"] == unver["kid"]:
            return {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    raise Halt(1011, "no key match found")


def validator(func):
    @wraps(func)
    def validate(*args, **kwargs):
        print(args)
        token = args[0].get('token')
        if not token:
            g.payload = None
            return
        try:
            res = requests.get(Config.AUTH0_API_BASE_URL+
                               "/.well-known/jwks.json")

            unverified = jwt.get_unverified_header(token)

            rsa_key = get_rsa(res.json(), unverified)

            payload = jwt.decode(
                token,
                rsa_key,
                audience=Config.AUTH0_CLIENT_ID,
                algorithms=["RS256"],
                issuer=f"https://{Config.AUTH0_DOMAIN}/"
            )
            # will only be set if no exceptions raised prior
            # indicating successful payload retrieval
            g.payload = payload
        except jwt.ExpiredSignatureError:
            g.error = Halt(1011, "expired token")
        except jwt.JWTClaimsError as e:
            g.error = Halt(1011, str(e))
        except KeyError:
            g.error = Halt(1011, "no authorization header provided")
        except ValueError:
            g.error = Halt(1011, "token or 'bearer' missing ")
        except Halt as res_error:
            g.error = res_error
        except Exception as e:
            g.error = Halt(1011, str(e))
        return func(*args, **kwargs)
    return validate


