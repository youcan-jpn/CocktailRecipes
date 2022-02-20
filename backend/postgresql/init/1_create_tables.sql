-- Postgresql

CREATE USER docker;

CREATE DATABASE docker;

GRANT ALL PRIVILEGES ON DATABASE docker TO docker;

-- change database
\c docker

-- TABLE
CREATE TABLE IF NOT EXISTS methods
(
    method_id       SERIAL      NOT NULL,
    method_name_jp  CHAR(4)     NOT NULL,
    method_name_en  CHAR(5)     NOT NULL,
    PRIMARY KEY (method_id)
);

CREATE TABLE IF NOT EXISTS cocktails
(
    cocktail_id         SERIAL      NOT NULL,
    cocktail_name_jp    CHAR(16)    NOT NULL,
    cocktail_name_en    CHAR(32),
    image_url           TEXT,
    method_id           INT         REFERENCES methods(method_id)   NOT NULL,
    cocktail_note_jp    TEXT        NOT NULL,
    cocktail_note_en    TEXT,
    PRIMARY KEY (cocktail_id)
);

CREATE TABLE IF NOT EXISTS recipes
(
    cocktail_id         INT         REFERENCES cocktails(cocktail_id)   NOT NULL,
    step_num            INT         NOT NULL,
    recipe_jp           TEXT        NOT NULL,
    recipe_en           TEXT,
    PRIMARY KEY (cocktail_id, step_num)
);

CREATE TABLE IF NOT EXISTS ingredients
(
    ingredient_id       SERIAL      NOT NULL,
    ingredient_name_jp  CHAR(32)    NOT NULL,
    ingredient_name_en  CHAR(64),
    PRIMARY KEY (ingredient_id)
);

CREATE TABLE IF NOT EXISTS cocktail_materials
(
    cocktail_id         INT         REFERENCES cocktails(cocktail_id)       NOT NULL,
    ingredient_id       INT         REFERENCES ingredients(ingredient_id)   NOT NULL,
    amount_jp           VARCHAR(32) NOT NULL,
    amount_en           VARCHAR(100),
    PRIMARY KEY (cocktail_id, ingredient_id)
);