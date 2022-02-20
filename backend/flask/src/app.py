import json

from sqlalchemy.orm import Session
from sqlalchemy import create_engine, update, delete
from flask_restful import Api, Resource
from flask import Flask, make_response, request


# constants
DATABASE_URL = "postgresql+psycopg2://user:pass@postgresql:5432/docker"
engine = create_engine(DATABASE_URL, encoding="utf-8", echo=True)


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["JSON_AS_ASCII"] = False

    api = Api(app)
    route_prefix: str = "/api"

    @api.representation("application/json")
    def output_json(data, code, headers):
        resp = make_response(json.dumps(data, ensure_ascii=False, indent=2),
                             code)
        resp.headers.extend(headers)
        return resp

    class epCocktails(Resource):
        def get(self):
            return 'Hello'

    # end points
    api.add_resource(epCocktails, f"{route_prefix}/cocktails")
    return app


app = create_app()
