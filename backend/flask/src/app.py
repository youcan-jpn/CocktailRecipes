import json

from sqlalchemy.orm import Session
from sqlalchemy import create_engine, update, delete, select
from flask_restful import Api, Resource
from flask import Flask, make_response, request

import src.functions.get_functions as get
from src.mappedClasses import (Cocktails, CocktailMaterials,
                               Ingredients, Recipes, Methods)

# constants
DATABASE_URL = "postgresql+psycopg2://user:pass@cocktail_postgresql:5432/docker"
COCKTAIL_NAME_MAX_LENGTH_JP = 16
COCKTAIL_NAME_MAX_LENGTH_EN = 32
INGREDIENT_NAME_MAX_LENGTH_JP = 32
INGREDIENT_NAME_MAX_LENGTH_EN = 64
engine = create_engine(DATABASE_URL, encoding="utf-8", echo=True)
route_prefix: str = "/api"


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["JSON_AS_ASCII"] = False

    api = Api(app)

    @api.representation("application/json")
    def output_json(data, code, headers):
        resp = make_response(json.dumps(data, ensure_ascii=False, indent=2),
                             code)
        resp.headers.extend(headers)
        return resp

    class epCocktails(Resource):
        def get(self):
            ret = []
            with Session(engine) as session:
                stmt = (select(Cocktails, Methods)
                        .join(Methods))
                rows = session.execute(stmt).all()
                for row in rows:
                    cocktail = {
                        "cocktail_id": row.Cocktails.cocktail_id,
                        "cocktail_name_jp": row.Cocktails.cocktail_name_jp,
                        "cocktail_name_en": row.Cocktails.cocktail_name_en,
                        "cocktail_img_url": row.Cocktails.image_url,
                        "method_id": row.Methods.method_id,
                        "method_name_jp": row.Methods.method_name_jp,
                        "method_name_en": row.Methods.method_name_en,
                    }
                    ret.append(cocktail)
            return ret

        def post(self):
            new_cocktail = request.json
            if "cocktail_name_jp" not in new_cocktail:
                return {"message": ("The JSON has to include the attribute "
                                    "'cocktail_name_jp'.")}, 400
            else:
                cocktail_name_jp = new_cocktail["cocktail_name_jp"]
            if len(cocktail_name_jp) > COCKTAIL_NAME_MAX_LENGTH_JP:
                return {"message": "'cocktail_name_jp' is too long."}, 400

            if "cocktail_name_en" not in new_cocktail:
                cocktail_name_en = ""
            else:
                cocktail_name_en = new_cocktail["cocktail_name_en"]
            if len(cocktail_name_en) > COCKTAIL_NAME_MAX_LENGTH_EN:
                return {"message": "'cocktail_name_en' is too long."}, 400

            if "cocktail_img_url" not in new_cocktail:
                cocktail_img_url = ""
            else:
                cocktail_img_url = new_cocktail["cocktail_img_url"]

            if "method_id" not in new_cocktail:
                return {"message": ("The JSON has to include the attribute "
                                    "'method_id'.")}, 400
            else:
                try:
                    method_id = int(new_cocktail["method_id"])
                except ValueError:
                    return {"message": "'method_id' has to be an integer."}, 400

            if int(method_id) not in [1, 2, 3, 4]:
                return {"message": ("method_id is one of the values "
                                    "[1 (build), 2 (stir), "
                                    "3 (shake), 4 (blend)].")}, 400

            if "cocktail_note_jp" not in new_cocktail:
                return {"message": ("The JSON has to include the attribute "
                                    "'cocktail_note_jp")}, 400
            else:
                cocktail_note_jp = new_cocktail["cocktail_note_jp"]

            if "cocktail_note_en" not in new_cocktail:
                cocktail_note_en = ""
            else:
                cocktail_note_en = new_cocktail["cocktail_note_en"]

            if "ingredients" not in new_cocktail:
                return {"message": ("The JSON has to include "
                                    "the attribute 'ingredients'.")}, 400
            else:
                ingredients = new_cocktail["ingredients"]
            if len(ingredients) < 1:
                return {"message": ("The recipe has to use "
                                    "at least one ingredient")}, 400

            if "procedures" not in new_cocktail:
                return {"message": ("The JSON has to include "
                                    "the attribute 'procedures'.")}, 400
            else:
                procedures = new_cocktail["procedures"]
            if len(new_cocktail["procedures"]) < 1:
                return {"message": ("The recipe has to contain "
                                    "at least one procedure")}, 400

            with Session(engine) as session:
                new_cocktail_obj = Cocktails(cocktail_name_jp=cocktail_name_jp,
                                             cocktail_name_en=cocktail_name_en,
                                             image_url=cocktail_img_url,
                                             method_id=method_id,
                                             cocktail_note_jp=cocktail_note_jp,
                                             cocktail_note_en=cocktail_note_en)
                session.add(new_cocktail_obj)
                session.flush()  # In order to get new cocktail's ID
                new_cocktail_id = new_cocktail_obj.cocktail_id

                for ingredient in ingredients:
                    if "ingredient_id" not in ingredient:
                        return {"message": ("The JSON has to include "
                                            "the attribute 'ingredient_id'.")}, 400
                    else:
                        try:
                            ingredient_id = int(ingredient["ingredient_id"])
                        except ValueError:
                            return {"message": ("'ingredient_id' has to be "
                                                "an integer.")}, 400

                    if "amount_jp" not in ingredient:
                        return {"message": ("The JSON has to include "
                                            "the attribute 'amount_jp'.")}, 400
                    else:
                        amount_jp = str(ingredient["amount_jp"])

                    if "amount_en" not in ingredient:
                        amount_en = ""
                    else:
                        amount_en = str(ingredient["amount_en"])

                    # check if specified ingredient_id exists
                    q = (session.query(Ingredients.ingredient_id)
                                .filter(Ingredients.ingredient_id == ingredient_id))  # noqa: E501
                    if not session.query(q.exists()).scalar():
                        return {"message":
                                ("The ingredient (ingredient_id = "
                                 f"{ingredient_id} does not exist.")}, 400

                    new_necessary_ingredient = CocktailMaterials(
                        cocktail_id=new_cocktail_id,
                        ingredient_id=ingredient_id,
                        amount_jp=amount_jp,
                        amount_en=amount_en,
                    )
                    session.add(new_necessary_ingredient)
                session.flush()

                step_num_list = []
                for procedure in procedures:
                    if "step_num" not in procedure:
                        return {"message": ("procedure has to include "
                                            "the attribute 'step_num'.")}, 400
                    else:
                        try:
                            step_num = procedure["step_num"]
                        except ValueError:
                            return {"message": ("step_num has to be "
                                                "an integer")}, 400
                    step_num_list.append(step_num)

                    if "recipe_jp" not in procedure:
                        return {"message": ("procedure has to include "
                                            "the attribute 'recipe_jp'.")}, 400
                    else:
                        recipe_jp = procedure["recipe_jp"]

                    if "recipe_en" not in procedure:
                        recipe_en = ""
                    else:
                        recipe_en = procedure["recipe_en"]

                    new_procedure = Recipes(cocktail_id=new_cocktail_id,
                                            step_num=step_num,
                                            recipe_jp=recipe_jp,
                                            recipe_en=recipe_en)
                    session.add(new_procedure)
                if len(step_num_list) != len(set(step_num_list)):
                    return {"message": "step_num has to be unique."}
                else:
                    session.commit()
                ret = get.cocktail_detail(session=session,
                                          cocktail_id=new_cocktail_id)
            return ret

    class epSpecifiedCocktails(Resource):
        def get(self, cocktail_id):
            with Session(engine) as session:
                ret = get.cocktail_detail(session, cocktail_id)
            return ret

        def put(self, cocktail_id):
            with Session(engine) as session:
                q = (session.query(Cocktails.cocktail_id)
                            .filter(Cocktails.cocktail_id == cocktail_id))
                if not session.query(q.exists()).scalar():
                    return {"message": ("The cocktail (cocktail_id="
                                        f"{cocktail_id}) does not exist")}, 400

                updated_cocktail = request.json
                if "cocktail_name_jp" not in updated_cocktail:
                    return {"message": ("The JSON has to include the attribute"
                                        " 'cocktail_name_jp'.")}, 400
                else:
                    cocktail_name_jp = updated_cocktail["cocktail_name_jp"]
                if len(cocktail_name_jp) > COCKTAIL_NAME_MAX_LENGTH_JP:
                    return {"message": "'cocktail_name_jp' is too long."}, 400

                if "cocktail_name_en" not in updated_cocktail:
                    return {"message": ("The JSON has to include the attribute"
                                        " 'cocktail_name_en'.")}, 400
                else:
                    cocktail_name_en = updated_cocktail["cocktail_name_en"]
                if len(cocktail_name_en) > COCKTAIL_NAME_MAX_LENGTH_EN:
                    return {"message": "'cocktail_name_en' is too long."}, 400

                if "cocktail_img_url" not in updated_cocktail:
                    return {"message": ("The JSON has to include the attribute"
                                        " 'cocktail_img_url'.")}, 400
                else:
                    cocktail_img_url = updated_cocktail["cocktail_img_url"]

                if "method_id" not in updated_cocktail:
                    return {"message": ("The JSON has to include the attribute"
                                        " 'method_id'.")}, 400
                else:
                    try:
                        method_id = int(updated_cocktail["method_id"])
                    except ValueError:
                        return {"message": ("'method_id' has to be an integer.")}, 400
                if method_id not in [1, 2, 3, 4]:
                    return {"message": ("method_id is one of the values "
                                        "[1 (build), 2 (stir), "
                                        "3 (shake), 4 (blend)].")}, 400

                if "cocktail_note_jp" not in updated_cocktail:
                    return {"message": ("The JSON has to include the attribute"
                                        " 'cocktail_note_jp")}, 400
                else:
                    cocktail_note_jp = updated_cocktail["cocktail_note_jp"]

                if "cocktail_note_en" not in updated_cocktail:
                    return {"message": ("The JSON has to include the attribute"
                                        " 'cocktail_note_en")}, 400
                else:
                    cocktail_note_en = updated_cocktail["cocktail_note_en"]

                if "ingredients" not in updated_cocktail:
                    return {"message": ("The JSON has to include "
                                        "the attribute 'ingredients'.")}, 400
                else:
                    ingredients = updated_cocktail["ingredients"]
                if len(ingredients) < 1:
                    return {"message": ("The recipe has to use "
                                        "at least one ingredient")}, 400

                if "procedures" not in updated_cocktail:
                    return {"message": ("The JSON has to include "
                                        "the attribute 'procedures'.")}, 400
                else:
                    procedures = updated_cocktail["procedures"]
                if len(updated_cocktail["procedures"]) < 1:
                    return {"message": ("The recipe has to contain "
                                        "at least one procedure")}, 400

                session.execute(update(Cocktails)
                                .where(Cocktails.cocktail_id == cocktail_id)
                                .values(
                                    cocktail_name_jp=cocktail_name_jp,
                                    cocktail_name_en=cocktail_name_en,
                                    image_url=cocktail_img_url,
                                    method_id=method_id,
                                    cocktail_note_jp=cocktail_note_jp,
                                    cocktail_note_en=cocktail_note_en
                                ))

                session.execute(delete(CocktailMaterials)
                                .where(CocktailMaterials.cocktail_id == cocktail_id))

                session.execute(delete(Recipes)
                                .where(Recipes.cocktail_id == cocktail_id))

                for ingredient in ingredients:
                    new_row = CocktailMaterials(
                        cocktail_id=cocktail_id,
                        ingredient_id=ingredient["ingredient_id"],  # TODO: Validation
                        amount_jp=ingredient["amount_jp"],
                        amount_en=ingredient["amount_en"]
                    )
                    session.add(new_row)

                for procedure in procedures:
                    new_row = Recipes(
                        cocktail_id=cocktail_id,
                        step_num=procedure["step_num"],
                        recipe_jp=procedure["recipe_jp"],
                        recipe_en=procedure["recipe_en"]
                    )
                    session.add(new_row)
                session.commit()
                ret = get.cocktail_detail(session, cocktail_id)
            return ret

    class epIngredients(Resource):
        def get(self):
            with Session(engine) as session:
                ret = []
                stmt = select(Ingredients).order_by(Ingredients.ingredient_id)
                rows = session.execute(stmt).all()
                for row in rows:
                    ingredient = {
                        "ingredient_id":
                        row.Ingredients.ingredient_id,
                        "ingredient_name_jp":
                            row.Ingredients.ingredient_name_jp,
                        "ingredient_name_en":
                            row.Ingredients.ingredient_name_en,
                    }
                    ret.append(ingredient)
            return ret

        def post(self):
            new_ingredient = request.json

            if "ingredient_name_jp" not in new_ingredient:
                return {"message": ("The JSON has to include"
                                    "the attribute 'ingredient_name_jp'")}, 400
            else:
                ingredient_name_jp = new_ingredient["ingredient_name_jp"]
            if len(ingredient_name_jp) > INGREDIENT_NAME_MAX_LENGTH_JP:
                return {"message":
                        ("The attribute 'ingredient_name_jp'"
                         "has to be shorter than {} chars."
                         ).format(INGREDIENT_NAME_MAX_LENGTH_JP)}, 400

            if "ingredient_name_en" not in new_ingredient:
                ingredient_name_en = ""
            else:
                ingredient_name_en = new_ingredient["ingredient_name_en"]
            if len(ingredient_name_en) > INGREDIENT_NAME_MAX_LENGTH_EN:
                return {"message":
                        ("The attribute 'ingredient_name_en'"
                         "has to be shorter than {} chars."
                         ).format(INGREDIENT_NAME_MAX_LENGTH_EN)}, 400

            with Session(engine) as session:
                new_row = Ingredients(ingredient_name_jp=ingredient_name_jp,
                                      ingredient_name_en=ingredient_name_en)
                session.add(new_row)
                session.commit()
                return {"ingredient_id":      new_row.ingredient_id,
                        "ingredient_name_jp": new_row.ingredient_name_jp,
                        "ingredient_name_en": new_row.ingredient_name_en}

    class epSpecifiedIngredient(Resource):
        def put(self, ingredient_id):
            modified_ingredient = request.json
            with Session(engine) as session:
                q = (session.query(Ingredients.ingredient_id)
                            .filter(Ingredients.ingredient_id == ingredient_id))  # noqa: E501
                if not session.query(q.exists()).scalar():
                    return {"message":
                            (f"The ingredient (ingredient_id = {ingredient_id}"
                             " does not exist.")}, 400

                if "ingredient_name_jp" not in modified_ingredient:
                    return {"message": ("The JSON has to include the attribute"
                                        " 'ingredient_name_jp'.")}, 400
                else:
                    new_ingredient_name_jp = modified_ingredient["ingredient_name_jp"]
                if len(new_ingredient_name_jp) > INGREDIENT_NAME_MAX_LENGTH_JP:
                    return {"message":
                            ("The attribute 'ingredient_name_jp'"
                             "has to be shorter than {} chars."
                             ).format(INGREDIENT_NAME_MAX_LENGTH_JP)}, 400

                if "ingredient_name_en" not in modified_ingredient:
                    new_ingredient_name_en = ""
                else:
                    new_ingredient_name_en = modified_ingredient["ingredient_name_en"]
                if len(new_ingredient_name_en) > INGREDIENT_NAME_MAX_LENGTH_EN:
                    return {"message":
                            ("The attribute 'ingredient_name_en'"
                             "has to be shorter than {} chars."
                             ).format(INGREDIENT_NAME_MAX_LENGTH_EN)}, 400

                session.execute(update(Ingredients)
                                .where(Ingredients.ingredient_id == ingredient_id)
                                .values(ingredient_name_jp=new_ingredient_name_jp,
                                        ingredient_name_en=new_ingredient_name_en))
                session.commit()
                return {"ingredient_id": ingredient_id,
                        "ingredient_name_jp": new_ingredient_name_jp,
                        "ingredient_name_en": new_ingredient_name_en}

        def delete(self, ingredient_id):
            with Session(engine) as session:
                q = (session.query(Ingredients.ingredient_id)
                            .filter(Ingredients.ingredient_id == ingredient_id))  # noqa: E501
                if not session.query(q.exists()).scalar():
                    return {"message":
                            (f"The ingredient (ingredient_id = {ingredient_id}"
                             " does not exist.")}, 400

                session.execute(delete(Ingredients)
                                .where(Ingredients.ingredient_id == ingredient_id))  # noqa: E501
                session.commit()
            return {"message": "The resource was deleted successfully"}, 204

    # end points
    api.add_resource(epCocktails, f"{route_prefix}/cocktails")
    api.add_resource(epSpecifiedCocktails, f"{route_prefix}/cocktails/<int:cocktail_id>")
    api.add_resource(epIngredients, f"{route_prefix}/ingredients")
    api.add_resource(epSpecifiedIngredient, f"{route_prefix}/ingredients/<int:ingredient_id>")

    return app


app = create_app()
