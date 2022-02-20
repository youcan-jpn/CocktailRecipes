\c docker

-- methods
INSERT INTO methods(method_name_jp, method_name_en) VALUES ('ビルド', 'Build');
INSERT INTO methods(method_name_jp, method_name_en) VALUES ('ステア', 'Stir');
INSERT INTO methods(method_name_jp, method_name_en) VALUES ('シェイク', 'Shake');
INSERT INTO methods(method_name_jp, method_name_en) VALUES ('ブレンド', 'Blend');

-- sample cocktail
INSERT INTO cocktails(cocktail_name_jp, cocktail_name_en, image_url, method_id, cocktail_note_jp, cocktail_note_en) VALUES ('ジントニック', 'gin tonic', 'undefined', '1', '17世紀にイギリス東インド会社の社員が、赴任中のインドでマラリア対策に飲んだ飲料が原型とされる。ベースを替えた、ラム・トニック、テキーラ・トニック（テコニック）、ウオツカ・トニックも飲まれている', 'Classic and easy, the gin and tonic (or G&T) is light and refreshing. It''s a simple mixed drink that requires just the two named ingredients and a hint of lime, all of which are natural flavor companions. This is a great choice for happy hour, dinner, or anytime you simply want an invigorating beverage.');

-- sample ingredients
INSERT INTO ingredients(ingredient_name_jp, ingredient_name_en) VALUES ('ジン', 'gin');
INSERT INTO ingredients(ingredient_name_jp, ingredient_name_en) VALUES ('トニックウォーター', 'tonic water');
INSERT INTO ingredients(ingredient_name_jp, ingredient_name_en) VALUES ('ライム', 'lime');

-- sample amount
INSERT INTO cocktail_materials VALUES (1, 1, '45ml', '2oz');
INSERT INTO cocktail_materials VALUES (1, 2, '適量', 'to taste');
INSERT INTO cocktail_materials VALUES (1, 3, '1切れ', '1slice');

--sample recipes
INSERT INTO recipes VALUES (1, 1, '氷を入れたグラスにジンを注いだあとトニックウォーターを加える。', 'In a highball glass filled with ice cubes, pour the gin, then top with tonic.');
INSERT INTO recipes VALUES (1, 2, '軽くかき混ぜる。', 'Gently stir to combine, but not so much so that you lose carbonation.');
INSERT INTO recipes VALUES (1, 3, 'ライムを添える。', 'Garnish with a lime wedge.');
