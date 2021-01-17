import os
import flask

from typing import Dict
from flask_restful import Api, Resource
from generate import (
    generate,
    encrypt,
    decrypt,
    QuotientException,
    IterationException,
    IntegerException,
    NegativeNumbersException,
    PrimeNumberException,
    TooSmallException,
    SameNumberException,
    TypeException
)

app = flask.Flask(__name__)
api = Api(app)


class GenerateToken(Resource):

    def post(self):

        try:
            data: Dict[str, int] = generate(**flask.request.get_json())
            response_code: int = 200
        except IntegerException as e:
            data: Dict[str, str] = {"Exception": str(e)}
            response_code: int = 400
        except IterationException as e:
            data: Dict[str, str] = {"Exception": str(e)}
            response_code: int = 401
        except QuotientException as e:
            data: Dict[str, str] = {"Exception": str(e)}
            response_code: int = 402
        except NegativeNumbersException as e:
            data: Dict[str, str] = {"Exception": str(e)}
            response_code: int = 403
        except PrimeNumberException as e:
            data: Dict[str, str] = {"Exception": str(e)}
            response_code: int = 404
        except TooSmallException as e:
            data: Dict[str, str] = {"Exception": str(e)}
            response_code: int = 405
        except SameNumberException as e:
            data: Dict[str, str] = {"Exception": str(e)}
            response_code: int = 406
        except TypeException as e:
            data: Dict[str, str] = {"Exception": str(e)}
            response_code: int = 407
        except Exception as e:
            data: Dict[str, str] = {"Exception": str(e)}
            response_code: int = 500

        return flask.make_response(flask.jsonify(data), response_code)


class Encrypt(Resource):
    def post(self):
        return flask.make_response(flask.jsonify(encrypt(**flask.request.get_json())))


class Decrypt(Resource):
    def post(self):
        return flask.make_response(decrypt(**flask.request.get_json()))


api.add_resource(GenerateToken, "/generate")
api.add_resource(Encrypt, "/encrypt")
api.add_resource(Decrypt, "/decrypt")

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
