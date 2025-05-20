from deepdiff import DeepDiff
import json


# 参数要求，需要对比的是json字符串，以及需要忽略的字段

def resp_diff(expected, realResp, ignore_keys):
    """
    比较两个 JSON 数据的差异，并忽略指定的键。

    :param expected: 第一个 JSON 数据（字符串或字典）
    :param realResp: 第二个 JSON 数据（字符串或字典）
    :param ignore_keys: 需要忽略的键的列表（例如 ["extra", "age"]）
    :return: 返回比较结果的描述和差异（如果有）
    """
    # 如果输入是字符串，将其解析为字典
    if isinstance(expected, str):
        dict1 = json.loads(expected)
    else:
        dict1 = expected

    if isinstance(realResp, str):
        dict2 = json.loads(realResp)
    else:
        dict2 = realResp

    # 构造 exclude_paths 参数
    exclude_paths = {f"root['{key}']" for key in ignore_keys}

    # print(f"ignore_keys{ignore_keys}")
    # # 使用 DeepDiff 进行比对
    # print(f"dict1{dict1}")
    # print(f"dict2{dict2}")
    # print(f"exclude_paths:{exclude_paths}")
    diff = DeepDiff(dict2, dict1, exclude_paths=exclude_paths)

    # 返回比较结果,直接返回diff需要对diff做判断

    return rename_diff_keys(diff)

def rename_diff_keys(diff_dict):
    """
    递归遍历 DeepDiff 结果，将 new_value/old_value 替换为自定义名称
    """
    if not isinstance(diff_dict, dict):
        return diff_dict

    renamed = {}
    for key, value in diff_dict.items():
        # 直接替换字段名
        if key == "new_value":
            renamed["expected"] = value
        elif key == "old_value":
            renamed["realResp"] = value
        # 递归处理嵌套结构
        elif isinstance(value, dict):
            renamed[key] = rename_diff_keys(value)
        elif isinstance(value, list):
            renamed[key] = [rename_diff_keys(item) if isinstance(item, dict) else item for item in value]
        else:
            renamed[key] = value
    return renamed

