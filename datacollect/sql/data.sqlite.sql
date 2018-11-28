-- 插入管理员(Administrator, Liang.Winson)
INSERT INTO user (username, password) VALUES  ('Administrator', 'pbkdf2:sha256:50000$pySt4Hfy$d1641a4f426bbe6753d4409328520c6c25536fc5a2740fcf1ff8b8bb5e2f6242');
--INSERT INTO post (title, body, author_id, created) VALUES  ('test title', 'test' || x'0a' || 'body', 1, '2018-01-01 00:00:00');
--INSERT INTO survey_types (name, fullname, index_page)
--VALUES ("汽车维修企业", "汽车维修企业污染源信息调查表", "car");
INSERT INTO survey_types (name, fullname, index_page)
VALUES ("餐饮企业", "餐饮企业污染源信息调查表", 'restaurant');
--INSERT INTO survey_types (name, fullname, index_page)
--VALUES ("医疗机构", "医疗机构污染源信息调查表", 'hospital');
--INSERT INTO survey_types (name, fullname, index_page)
--VALUES ("加油站", "加油站污染源信息调查表", 'gas');
--INSERT INTO survey_types (name, fullname, index_page)
--VALUES ("检测机构、实验室、学校和物业公司",
--"检测机构、实验室、学校和物业公司危险废物信息调查表", 'org');
--INSERT INTO survey_types (name, fullname, index_page)
--VALUES ("县域城镇生活", "县域城镇生活污染调查表", 'life');
--INSERT INTO survey_types (name, fullname, index_page)
--VALUES ("入河（海）排污口", "入河（海）排污口信息调查表", 'river');