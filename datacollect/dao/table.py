# coding: utf-8


class Table(object):
    TABLE_NAME = ""
    TABLE_FIELDS = [
    ]


class TableNames:
    ENT_RESTAURANT_SURVEY = "ent_restaurant_survey"


class RestaurantTable(Table):
    TABLE_NAME = TableNames.ENT_RESTAURANT_SURVEY
    TABLE_FIELDS = [
        ("id", "唯一键ID"),
        ("uniform_credit_code", "社会统一信用代码"),
        ("origin_org_code", "原组织机构代码号"),
        ("ent_name", "单位名称"),
        ("ent_former_name", "单位曾用名"),
        ("province", "省"),
        ("city", "市"),
        ("district", "地（区，市，州，盟）"),
        ("town", "乡镇"),
        ("address", "详细地址"),
        ("region_code", "区划代码"),
        ("longitude", "经度"),
        ("latitude", "纬度"),
        ("lon_d", "经度(度)"),
        ("lon_m", "经度(分)"),
        ("lon_s", "经度(秒)"),
        ("lat_d", "纬度(度)"),
        ("lat_m", "纬度(分)"),
        ("lat_s", "纬度(秒)"),
        ("legal_person", "法人代表"),
        ("open_date", "开业(成立)时间"),
        ("ent_contact", "企业联系人"),
        ("ent_phone", "企业联系电话"),
        ("run_normally", "是否正常运营"),
        ("restaurant_type", "餐饮类型"),
        ("burner_num", "炉头数"),
        ("customer_capacity", "可容纳就餐人数"),
        ("employee_num", "员工人数"),
        ("annual_turnover", "年营业额"),
        ("ent_area", "经营面积"),
        ("cooking_oil", "食用油使用量"),
        ("water_used", "年用水量"),
        ("water_waster_emit", "年废水排放量"),
        ("oil_device", "是否有隔油设施"),
        ("water_cod", "废水化学需氧量浓度"),
        ("water_nh4", "废水氨氮浓度"),
        ("water_tp", "废水总磷浓度"),
        ("water_oil", "废水动植物油浓度"),
        ("water_monitor", "是否在线监测"),
        ("gas_device", "是否有油烟净化设施"),
        ("gas_emission_vol", "油烟排放风量"),
        ("device_runtime", "设施年运行小时数"),
        ("gas_solid", "油烟颗粒物浓度"),
        ("not_ch4", "非甲烷浓度"),
        ("gas_monitor", "是否有油烟在线监测"),
        ("kitchen_waster_volume", "餐厨垃圾量"),
        ("kitchen_waster_gone", "餐厨垃圾去向"),
        ("survey_person", "调查人"),
        ("contact", "联系人"),
        ("survey_date", "调查日期"),
        ("updated_by", "更改人"),
        ("updated_date", "更改日期"),
    ]
