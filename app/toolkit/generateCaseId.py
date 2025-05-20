import uuid


def generate_caseid():
    """
    生成不重复的 caseid
    :return: 以字符串形式返回生成的唯一 caseid
    """
    return str(uuid.uuid4())
