-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS ent_restaurant_survey;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

-- 餐饮企业污染源信息调查表
CREATE TABLE ent_restaurant_survey (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  uniform_credit_code TEXT,  -- 社会统一信用代码
  origin_org_code TEXT,  -- 原组织机构代码号
  ent_name TEXT, -- 单位名称
  ent_former_name TEXT, -- 单位曾用名
  province TEXT,  -- 省
  city TEXT, -- 市
  district TEXT, -- 地（区，市，州，盟）
  town TEXT,  -- 乡镇
  address TEXT,
  region_code TEXT,
  longitude_d NUMERIC,
  longitude_m NUMERIC,
  longitude_s NUMERIC,
  latitude_d NUMERIC,
  latitude_m NUMERIC,
  latitude_s NUMERIC,
  legal_person TEXT, -- 法人代表
  ent_contact TEXT, -- 企业联系人
  ent_phone TEXT, -- 企业联系电话
  run_normally TEXT, -- 是否正常运营
  restaurant_type TEXT, -- 餐饮类型
  burner_num NUMERIC, -- 炉头数
  customer_capacity NUMERIC, -- 可容纳就餐人数
  employee_num NUMERIC, -- 员工人数
  annual_turnover NUMERIC, -- 年营业额
  ent_area NUMERIC, -- 经营面积
  cooking_oil NUMERIC, -- 食用油使用量
  water_used NUMERIC, -- 年用水量
  oil_device TEXT, -- 是否有隔油设施
  water_cod NUMERIC, -- 废水化学需氧量浓度
  water_nh4 NUMERIC, -- 废水氨氮浓度
  water_tp NUMERIC, -- 废水总磷浓度
  water_oil NUMERIC, -- 废水动植物油浓度
  water_monitor TEXT, -- 是否在线监测
  gas_device TEXT, -- 是否有油烟净化设施
  gas_emission_vol NUMERIC, -- 油烟排放风量
  device_runtime NUMERIC, -- 设施年运行小时数
  gas_solid NUMERIC, -- 油烟颗粒物浓度
  not_ch4 NUMERIC, -- 非甲烷浓度
  gas_monitor TEXT, -- 是否有油烟在线监测
  kitchen_waster_volume NUMERIC, -- 餐厨垃圾量
  kitchen_waster_gone TEXT, -- 餐厨垃圾去向
  survey_person TEXT, -- 调查人
  contact TEXT, -- 联系人
  survey_date TIMESTAMP,
  updated_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT NOT NULL
);
