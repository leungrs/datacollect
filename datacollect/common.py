# coding: utf-8

SUCCESS = "ok"
FAIL = "fail"

class Result:
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