from typing import Dict, Tuple, Any
from coopui.cli.typeToRequestMapping import CLI_TYPE_TO_REQUEST_MAPPING as ctrm


class CliParameterRequestObj:

    @classmethod
    def resolve_request(cls, type, **kwargs):
        callback, sig_params = ctrm[type]
        if callback is None:
            return None

        return callback(**kwargs)

    @classmethod
    def request(cls, parameter_request_dict: Dict[str, Tuple], allow_partial: bool = True) -> Dict[str, Any]:
        ret = {}
        for param_name, request_definition in parameter_request_dict.items():

            if isinstance(request_definition, Tuple) and len(request_definition) >= 2:
                param_type = request_definition[0]
                request_args = request_definition[1] if request_definition[1] else {}
            elif isinstance(request_definition, Tuple) and len(request_definition) == 1:
                param_type = request_definition[0]
                request_args = {}
            else:
                param_type = request_definition
                request_args = {}

            ret[param_name] = cls.resolve_request(param_type, **request_args)

            # Break early if fail to get a value when not allowed
            if ret[param_name] is None and not allow_partial:
                return None

        return ret


if __name__ == "__main__":
    from enum import Enum
    from typing import List, Dict

    class MyEnum(Enum):
        a=1
        b=2
        c=3

    my_dic = {1: 'i',
              2: 'j',
              3: 'k'}
    my_list = ['l', 'm', 'n']
    requested_params = {"str1": (str, {"prompt": "Try the str: "}),
                        "int1": (int, {"prompt": "Try the int: "}),
                        "float1": (float, {"prompt": "Try the float: "}),
                        "myenum": (Enum, {"prompt": "Select Enum: ", "enum": MyEnum}),
                        "mydic": (Dict, {"prompt": "Select from dic", "selectionDict": my_dic}),
                        "my_list": (List, {"prompt": "Select from list", "selectionList": my_list})
                        }

    ret = CliParameterRequestObj.request(parameter_request_dict=requested_params, allow_partial=False)

    if ret is not None:
        for k, v in ret.items():
            print(f"{k}: {v}")
    else:
        print(f"Did not get params")