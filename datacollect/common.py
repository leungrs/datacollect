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


def create_china_admin_tree(file_path):
    root = AdminNode("中国", -1)
    with open(file_path, "r", encoding="utf-8") as fp:
        obj = json.load(fp)
        init_admin_tree(root, obj)
    return root


class AdminNodeHandler(object):
    def __init__(self):
        self.root = create_china_admin_tree(os.path.join(DATA_FOLDER, "address4.json"))

        self.level_nodes = [[], [], [], []]

        for node in self.root.children:
            level = node.level
            self.level_nodes[level].append(node)

        self.select_by_name(name="广东省")
        self.select_by_name(level=1, name="深圳市")
        self.select_by_name(level=2, name="福田区")

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

if __name__ == '__main__':
    hd = AdminNodeHandler()
    hd.print()

