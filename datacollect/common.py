# coding: utf-8

import os
import json
from datacollect.config import DATA_FOLDER

SUCCESS = "ok"
FAIL = "fail"


class Result(object):
    """"""

    def __init__(self, status=SUCCESS, data=None, message=""):
        self.status = status
        self.message = message
        self.data = data

    def to_json(self):
        return {
            "status": self.status,
            "message": self.message,
            "data": self.data
        }


def to_type(obj, type_obj=str, default=0):
    try:
        if isinstance(type_obj, str):
            if type_obj == "float":
                type_obj = float
            elif type_obj == "int":
                type_obj = int
            elif type_obj == "str":
                type_obj = str
                default = ""
            else:
                pass

        if type_obj is str:
            default = ""

        return type_obj(obj)
    except:
        return default


def to_d_m_s(val):
    """十进制转换成度分秒"""
    i_d = int(val)
    m = (val - i_d) * 60
    i_m = int(m)
    i_s = int((m - i_m) * 60)
    return i_d, i_m, i_s


class AdminNode(object):
    def __init__(self, name, level=1):
        self.name = name
        self.level = level
        self.children = []
        self.parent = None
        self.selected = False

    def add_child(self, child):
        self.children.append(child)
        child.parent = self
        child.level = self.level + 1


def init_admin_tree(node, obj):
    for name, value in obj.items():
        child_node = AdminNode(name)
        node.add_child(child_node)
        if isinstance(value, list):
            for item in value:
                child_node.add_child(AdminNode(item))
        else:
            init_admin_tree(child_node, value)


def create_admin_tree(province=None, city=None, district=None, town=None):
    file_path = os.path.join(DATA_FOLDER, "address4.json")
    root = AdminNode("中国", -1)
    with open(file_path, "r", encoding="utf-8") as fp:
        obj = json.load(fp)
        if province is not None:
            filter_by_key(obj, province)
            province_obj = obj.get(province)
            if city is not None:
                filter_by_key(province_obj, city)
                city_obj = province_obj.get(city)
                if district is not None:
                    filter_by_key(city_obj, district)
                    district_obj = city_obj.get(district)
                    if town is not None:
                        filter_by_key(district_obj, town)
        init_admin_tree(root, obj)
    return root


def filter_by_key(obj, key):
    if not obj:
        return
    for k in list(obj.keys()):
        if k != key:
            obj.pop(k)


class AdminNodeHandler(object):
    def __init__(self, province=None, city=None, district=None, town=None):
        self.root = create_admin_tree(province, city, district, town)
        self.level_nodes = [[], [], [], []]
        for node in self.root.children:
            level = node.level
            self.level_nodes[level].append(node)
        self.select_by_index()

    def select_by_index(self, level=0, index=0):
        self.select_node(self.level_nodes[level][index])

    def select_by_name(self, level=0, name="北京市"):
        for node in self.level_nodes[level]:
            if node.name == name:
                self.select_node(node)
                break

    def select_node(self, selected_node):
        selected_node.selected = True
        level = selected_node.level
        while level < 3:
            self.level_nodes[level + 1].clear()
            level += 1

        level_nodes = self.level_nodes[selected_node.level]
        for node in level_nodes:
            if node != selected_node:
                node.selected = False

        if selected_node.children:
            for node in selected_node.children:
                self.level_nodes[selected_node.level+1].append(node)
            self.select_node(selected_node.children[0])

    def select_by_item(self, item):
        if not item:
            self.select_by_index()
            return

        province = item["province"]
        self.select_by_name(0, name=province)
        city = item["city"]
        self.select_by_name(1, name=city)
        district = item["district"]
        self.select_by_name(2, name=district)
        town = item["town"]
        self.select_by_name(3, name=town)

    def get_admins(self):
        return {
            "p": self.level_nodes[0],
            "c": self.level_nodes[1],
            "d": self.level_nodes[2],
            "t": self.level_nodes[3],
        }

    def print(self):
        i = 0
        while 1:
            l1 = self.level_nodes[0][i:i+1]
            l2 = self.level_nodes[1][i:i+1]
            l3 = self.level_nodes[2][i:i+1]
            l4 = self.level_nodes[3][i:i+1]
            if l1 or l2 or l3 or l4:
                print("%-20s %-20s %-20s %-20s " % (
                    "" if not l1 else l1[0].name + "+" if l1[0].selected else l1[0].name,
                    "" if not l2 else l2[0].name + "+" if l2[0].selected else l2[0].name,
                    "" if not l3 else l3[0].name + "+" if l3[0].selected else l3[0].name,
                    "" if not l4 else l4[0].name + "+" if l4[0].selected else l4[0].name,
                ))
                i += 1
            else:
                break


ADMIN_HANDLER = AdminNodeHandler("广东省", "深圳市", "福田区", None)


if __name__ == '__main__':
    hd = AdminNodeHandler()
    hd.print()

