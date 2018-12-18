-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS user_last_cache;
DROP TABLE IF EXISTS survey_types;
DROP TABLE IF EXISTS ent_restaurant_survey;
DROP TABLE IF EXISTS hospital_survey;

-- 用户信息表
CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  role TEXT NOT NULL default 'user',
  password TEXT NOT NULL
);
-- 用户上次操作系统的缓存信息表
CREATE TABLE user_last_cache (
  user_id INTEGER NOT NULL,
  survey_type_id INTEGER NOT NULL -- 上次操作的调查表类型
);
-- 调查表类型表
CREATE TABLE survey_types (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,  -- 简称
  fullname TEXT NOT NULL, -- 全称
  index_page TEXT NOT NULL,  -- 对应的首页
  attrib1 TEXT,
  attrib2 TEXT,
  attrib3 TEXT
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
  longitude REAL,
  latitude REAL,
  lon_d REAL,
  lon_m REAL,
  lon_s REAL,
  lat_d REAL,
  lat_m REAL,
  lat_s REAL,
  legal_person TEXT, -- 法人代表
  open_date TEXT,  -- 开业(成立)时间
  ent_contact TEXT, -- 企业联系人
  ent_phone TEXT, -- 企业联系电话
  run_normally TEXT, -- 是否正常运营
  restaurant_type TEXT, -- 餐饮类型
  burner_num INT, -- 炉头数
  customer_capacity INT, -- 可容纳就餐人数
  employee_num INT, -- 员工人数
  annual_turnover REAL, -- 年营业额
  ent_area REAL, -- 经营面积
  cooking_oil REAL, -- 食用油使用量
  water_used REAL, -- 年用水量
  water_waster_emit REAL, -- 年废水排放量
  oil_device TEXT, -- 是否有隔油设施
  water_cod REAL, -- 废水化学需氧量浓度
  water_nh4 REAL, -- 废水氨氮浓度
  water_tp REAL, -- 废水总磷浓度
  water_oil REAL, -- 废水动植物油浓度
  water_monitor TEXT, -- 是否在线监测
  gas_device TEXT, -- 是否有油烟净化设施
  gas_emission_vol REAL, -- 油烟排放风量
  device_runtime REAL, -- 设施年运行小时数
  gas_solid REAL, -- 油烟颗粒物浓度
  not_ch4 REAL, -- 非甲烷浓度
  gas_monitor TEXT, -- 是否有油烟在线监测
  kitchen_waster_volume REAL, -- 餐厨垃圾量
  kitchen_waster_gone TEXT, -- 餐厨垃圾去向
  survey_person TEXT, -- 调查人
  contact TEXT, -- 联系人
  survey_date TIMESTAMP,
  updated_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT NOT NULL
);
-- 医疗机构污染源信息调查表
CREATE TABLE hospital_survey (
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
  longitude REAL,
  latitude REAL,
  lon_d REAL,
  lon_m REAL,
  lon_s REAL,
  lat_d REAL,
  lat_m REAL,
  lat_s REAL,
  legal_person TEXT, -- 法人代表
  open_date TEXT,  -- 开业(成立)时间
  ent_contact TEXT, -- 企业联系人
  ent_phone TEXT, -- 企业联系电话
  run_normally TEXT, -- 是否正常运营
  bed_num INT, -- 床位数
  patient_num INT, -- 年就诊人数
  annual_turnover REAL, -- 年营业额
  building_area REAL, -- 建筑面积
  water_used REAL, -- 年用水量
  water_process_name TEXT, -- 废水处理工艺名称
  water_waster_emit REAL, -- 年废水排放量
  water_cod REAL, -- 废水化学需氧量浓度
  water_bod REAL, -- BOD浓度
  water_fecal_coliform REAL, -- 粪大肠菌群
  water_monitor TEXT, -- 是否在线监测
  waster1_type TEXT, -- 医疗废物名称，类别
  waster1_annual REAL, -- 年产生量
  waster1_jcz REAL, -- 交持证单位量
  waster2_type TEXT, -- 医疗废物名称，类别
  waster2_annual REAL, -- 年产生量
  waster2_jcz REAL, -- 交持证单位量
  waster3_type TEXT, -- 医疗废物名称，类别
  waster3_annual REAL, -- 年产生量
  waster3_jcz REAL, -- 交持证单位量
  survey_person TEXT, -- 调查人
  contact TEXT, -- 联系人
  survey_date TIMESTAMP,
  updated_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT NOT NULL
);

