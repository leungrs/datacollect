-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS user_last_cache;
DROP TABLE IF EXISTS survey_types;
DROP TABLE IF EXISTS restaurant_survey;
DROP TABLE IF EXISTS hospital_survey;
DROP TABLE IF EXISTS car_survey;
DROP TABLE IF EXISTS gas_survey;
DROP TABLE IF EXISTS org_survey;
DROP TABLE IF EXISTS life_survey;
DROP TABLE IF EXISTS river_survey;

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
CREATE TABLE restaurant_survey (
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
-- 汽车维修企业污染源信息调查表
CREATE TABLE car_survey (
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
  ent_type TEXT, -- 汽修企业类型
  car_num INT, -- 洗车车位数
  house_num INT, -- 烤漆房个数
  annual_turnover REAL, -- 年营业额
  building_area REAL, -- 经营面积
  oil_paint_used REAL, --  油性漆用量
  water_paint_used REAL, -- 水性漆用量
  thinner_used REAL, -- 天那水用量
  water_used REAL, -- 年用水量
  water_waster_emit REAL, -- 年废水排放量
  water_process_name TEXT, -- 废水处理工艺名称
  oil_device TEXT, -- 是否有隔油沉淀设施
  water_cod REAL, -- 废水化学需氧量浓度
  water_nh4 REAL, -- 废水氨氮浓度
  water_tp REAL, -- 废水总磷浓度
  water_oil REAL, -- 石油类浓度
  water_monitor TEXT, -- 是否在线监测
  gas_process_name TEXT, -- 有机废气处理工艺名称
  gas_emission_vol REAL, -- 有机废气排放风量
  device_runtime REAL, -- 设施年运行小时数
  benzene REAL, -- 苯浓度
  methylbenzene REAL, -- 甲苯浓度
  dimethylbenzene REAL, -- 二甲苯浓度
  not_ch4 REAL, -- 非甲烷浓度
  voc_total REAL, -- 总VOC浓度
  gas_monitor TEXT, -- 是否安装在线监测
  waster1_type TEXT, -- 危险废物名称，类别
  waster1_annual REAL, -- 年产生量
  waster1_jcz REAL, -- 交持证单位量
  waster2_type TEXT, -- 危险废物名称，类别
  waster2_annual REAL, -- 年产生量
  waster2_jcz REAL, -- 交持证单位量
  waster3_type TEXT, -- 危险废物名称，类别
  waster3_annual REAL, -- 年产生量
  waster3_jcz REAL, -- 交持证单位量
  survey_person TEXT, -- 调查人
  contact TEXT, -- 联系人
  survey_date TIMESTAMP,
  updated_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT NOT NULL
);
-- 加油站污染源信息调查表
CREATE TABLE gas_survey (
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
  gasoline_name TEXT, -- 所属加油站名称
  run_normally TEXT, -- 是否正常运营
  gasoline_total REAL, -- 汽油总罐容
  gasoline_sale REAL, -- 汽油年销售量
  gasoline_recycle_stage TEXT, -- 汽油回收阶段
  gasoline_has_device TEXT, -- 有无排放处理装置
  gasoline_has_monitor TEXT, -- 有无在线监测系统
  gasoline_device_finished TEXT, -- 汽油回收装置改造完成时间
  diesel_total REAL, -- 柴油总罐容
  diesel_sale REAL, -- 柴油年销售量
  waster1_type TEXT, -- 危险废物名称，类别
  waster1_annual REAL, -- 年产生量
  waster1_jcz REAL, -- 交持证单位量
  waster2_type TEXT, -- 危险废物名称，类别
  waster2_annual REAL, -- 年产生量
  waster2_jcz REAL, -- 交持证单位量
  waster3_type TEXT, -- 危险废物名称，类别
  waster3_annual REAL, -- 年产生量
  waster3_jcz REAL, -- 交持证单位量
  survey_person TEXT, -- 调查人
  contact TEXT, -- 联系人
  survey_date TIMESTAMP,
  updated_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT NOT NULL
);
-- 检测机构、实验室、学校和物业公司危险废物信息调查表
CREATE TABLE org_survey (
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
  waster1_type TEXT, -- 危险废物名称，类别
  waster1_annual REAL, -- 年产生量
  waster1_jcz REAL, -- 交持证单位量
  waster2_type TEXT, -- 危险废物名称，类别
  waster2_annual REAL, -- 年产生量
  waster2_jcz REAL, -- 交持证单位量
  waster3_type TEXT, -- 危险废物名称，类别
  waster3_annual REAL, -- 年产生量
  waster3_jcz REAL, -- 交持证单位量
  survey_person TEXT, -- 调查人
  contact TEXT, -- 联系人
  survey_date TIMESTAMP,
  updated_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT NOT NULL
);
-- 县域城镇生活污染调查表
CREATE TABLE life_survey (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  province TEXT,  -- 省
  city TEXT, -- 市
  district TEXT, -- 地（区，市，州，盟）
  town TEXT,  -- 乡镇
  address TEXT,
  region_code TEXT,
  total_population REAL, -- 全县人口
  city_population REAL, -- 县城人口
  transient_population REAL, -- 暂住人口
  city_transient_population REAL, -- 县城暂住人口
  public_service_water REAL, -- 公共服务用水量
  family_water REAL, -- 居民家庭用水量
  free_water REAL, -- 生活用水量（免费供水）
  water_population REAL, -- 用水人口
  centralize_heating_area REAL, -- 集中供热面积
  manufactured_gas REAL, -- 人工煤气销售气量
  natural_gas REAL, -- 天然气销售气量
  liquefied_petroleum_gas REAL, -- 液化石油气销售气量
  town_count INT, -- 建制镇个数
  town_population REAL, -- 建成区常住人口
  town_water REAL, -- 建成区生活用水量
  town_water_population REAL, -- 建成区用水人口
  town_average_water REAL, -- 建成区人均日生活用水量
  country_average_water REAL, -- 村庄人均日生活用水量
  survey_person TEXT, -- 调查人
  contact TEXT, -- 联系人
  survey_date TIMESTAMP,
  updated_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT NOT NULL
);
-- 入河（海）排污口信息调查表
CREATE TABLE river_survey (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  outfall_name TEXT, -- 排污口名称
  outfall_code TEXT, -- 排污口编码
  outfall_category TEXT, -- 排污口类别
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
  install_unit TEXT, -- 设置单位
  outfall_size TEXT, -- 排污口规模
  outfall_type TEXT, -- 排污口类型
  outfall_way TEXT, -- 入河（海）方式
  receiving_water_name TEXT, -- 受纳水体名称
  receiving_water_code TEXT, -- 受纳水体代码
  monitor_time01 TEXT,
  monitor_time02 TEXT,
  monitor_time03 TEXT,
  monitor_time04 TEXT,
  monitor_time05 TEXT,
  monitor_time06 TEXT,
  monitor_time07 TEXT,
  monitor_time08 TEXT,
  monitor_time09 TEXT,
  monitor_time10 TEXT,
  monitor_time11 TEXT,
  monitor_time12 TEXT,
  waste_water01 REAL,
  waste_water02 REAL,
  waste_water03 REAL,
  waste_water04 REAL,
  waste_water05 REAL,
  waste_water06 REAL,
  waste_water07 REAL,
  waste_water08 REAL,
  waste_water09 REAL,
  waste_water10 REAL,
  waste_water11 REAL,
  waste_water12 REAL,
  cod01 REAL,
  cod02 REAL,
  cod03 REAL,
  cod04 REAL,
  cod05 REAL,
  cod06 REAL,
  cod07 REAL,
  cod08 REAL,
  cod09 REAL,
  cod10 REAL,
  cod11 REAL,
  cod12 REAL,
  five_day01 REAL,
  five_day02 REAL,
  five_day03 REAL,
  five_day04 REAL,
  five_day05 REAL,
  five_day06 REAL,
  five_day07 REAL,
  five_day08 REAL,
  five_day09 REAL,
  five_day10 REAL,
  five_day11 REAL,
  five_day12 REAL,
  nh4n01 REAL,
  nh4n02 REAL,
  nh4n03 REAL,
  nh4n04 REAL,
  nh4n05 REAL,
  nh4n06 REAL,
  nh4n07 REAL,
  nh4n08 REAL,
  nh4n09 REAL,
  nh4n10 REAL,
  nh4n11 REAL,
  nh4n12 REAL,
  tn01 REAL,
  tn02 REAL,
  tn03 REAL,
  tn04 REAL,
  tn05 REAL,
  tn06 REAL,
  tn07 REAL,
  tn08 REAL,
  tn09 REAL,
  tn10 REAL,
  tn11 REAL,
  tn12 REAL,
  tp01 REAL,
  tp02 REAL,
  tp03 REAL,
  tp04 REAL,
  tp05 REAL,
  tp06 REAL,
  tp07 REAL,
  tp08 REAL,
  tp09 REAL,
  tp10 REAL,
  tp11 REAL,
  tp12 REAL,
  oil01 REAL,
  oil02 REAL,
  oil03 REAL,
  oil04 REAL,
  oil05 REAL,
  oil06 REAL,
  oil07 REAL,
  oil08 REAL,
  oil09 REAL,
  oil10 REAL,
  oil11 REAL,
  oil12 REAL,
  other01 REAL,
  other02 REAL,
  other03 REAL,
  other04 REAL,
  other05 REAL,
  other06 REAL,
  other07 REAL,
  other08 REAL,
  other09 REAL,
  other10 REAL,
  other11 REAL,
  other12 REAL,
  survey_person TEXT, -- 调查人
  contact TEXT, -- 联系人
  survey_date TIMESTAMP,
  updated_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT NOT NULL
);
