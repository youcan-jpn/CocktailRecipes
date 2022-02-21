from sqlalchemy import (Table, MetaData, create_engine)
from sqlalchemy.orm import declarative_base

DATABASE_URI = "postgresql+psycopg2://user:pass@cocktail_postgresql:5432/docker"

engine = create_engine(DATABASE_URI, encoding="utf-8", echo=True)

Base = declarative_base()
metadata_obj = MetaData()

# Table Reflections
# create Table object from existing RDB
methods_table = Table("methods", metadata_obj, autoload_with=engine)
cocktails_table = Table("cocktails", metadata_obj, autoload_with=engine)
ingredients_table = Table("ingredients", metadata_obj, autoload_with=engine)
cocktail_materials_table = Table("cocktail_materials",
                                 metadata_obj, autoload_with=engine)
recipes_table = Table("recipes", metadata_obj, autoload_with=engine)


class Methods(Base):
    __table__ = methods_table


class Cocktails(Base):
    __table__ = cocktails_table


class Ingredients(Base):
    __table__ = ingredients_table


class CocktailMaterials(Base):
    __table__ = cocktail_materials_table


class Recipes(Base):
    __table__ = recipes_table
