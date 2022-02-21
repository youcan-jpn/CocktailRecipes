from sqlalchemy import select
from sqlalchemy.orm import Session

from ..mappedClasses import (Cocktails, CocktailMaterials,
                             Recipes, Methods, Ingredients)


# ----------------------------
# GET /cocktails/{cocktail_id}
# ----------------------------
def cocktail_detail(session: Session, cocktail_id: int) -> dict:
    """
    A function that is used for the end point 'cocktails/{cocktail_id}'

    Parameters
    ----------
    session : sqlalchemy.orm.Session
    cocktail_id : int
        cocktail_id of the cocktail you want to know details

    Return
    ------
    ret : dict
        A dictionary that contains cocktail information.
        (you can get more information in OAS)
    """
    ret = {}

    stmt1 = (select(Cocktails, Methods)
             .where(Cocktails.cocktail_id == cocktail_id)
             .join(Methods))
    row = (session.execute(stmt1).first())
    ret["cocktail_id"] = cocktail_id
    ret["cocktail_name_jp"] = row.Cocktails.cocktail_name_jp
    ret["cocktail_name_en"] = row.Cocktails.cocktail_name_en
    ret["cocktail_img_url"] = row.Cocktails.image_url
    ret["method_id"] = row.Cocktails.method_id
    ret["method_name_jp"] = row.Methods.method_name_jp
    ret["method_name_en"] = row.Methods.method_name_en
    ret["cocktail_note_jp"] = row.Cocktails.cocktail_note_jp
    ret["cocktail_note_en"] = row.Cocktails.cocktail_note_en
    ret["ingredients"] = []
    ret["procedures"] = []

    stmt2 = (select(CocktailMaterials, Ingredients)
             .order_by(CocktailMaterials.ingredient_id)
             .where(CocktailMaterials.cocktail_id == cocktail_id)
             .join(Ingredients))
    material_rows = (session.execute(stmt2).all())
    for row in material_rows:
        material = {}
        material["ingredient_id"] = row.Ingredients.ingredient_id
        material["ingredient_name_jp"] = row.Ingredients.ingredient_name_jp
        material["ingredient_name_en"] = row.Ingredients.ingredient_name_en
        material["amount_jp"] = row.CocktailMaterials.amount_jp
        material["amount_en"] = row.CocktailMaterials.amount_en
        ret["ingredients"].append(material)

    stmt3 = (select(Recipes)
             .order_by(Recipes.step_num)
             .where(Recipes.cocktail_id == cocktail_id))
    procedure_rows = (session.execute(stmt3).all())
    for row in procedure_rows:
        recipe = {}
        recipe["step_num"] = row.Recipes.step_num
        recipe["recipe_jp"] = row.Recipes.recipe_jp
        recipe["recipe_en"] = row.Recipes.recipe_en
        ret["procedures"].append(recipe)

    return ret
