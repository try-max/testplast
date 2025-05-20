import json

import pymysql
from flask import Blueprint
from flask import request

from app.api.common.utils import res, resCase
from app.api.schema.register_sha import reg_args_valid
from app.dbutil.dbUtils import select_all, update_one, insert_one_pk
from app.toolkit.generateCaseId import generate_caseid
from app.toolkit.getDate import get_current_time, get_current_time_str

case_bp = Blueprint('case_api', __name__, url_prefix='/api/case')


@case_bp.route('/getAllCase', methods=['GET', 'POST'])
# @jwt_required()
def get_all_cases():
    try:

        sql = "SELECT * FROM test_cases"
        result = select_all(sql)

        return resCase(data=result)

    except:
        return resCase(success=False, message='服务器繁忙！', code=500)


#编辑已有用例的ID
@case_bp.route('/caseEdit', methods=['GET', 'POST'])
# @jwt_required()
def caseEdit():
    data = request.get_json()
    if not data:
        # 返回明确的错误信息，避免引用未定义的 result
        # 400 Bad Request
        return res(message="请求数据为空", success=False, code=400)

    try:
        # 打印接收到的数据（调试用）
        # print("Received data:", data)

        # 提取必要字段（建议增加字段存在性校验）
        id = data.get('id')
        # method = data.get('method')
        # url = data.get('url')
        # params = data.get('params', {})  # 默认空字典
        # headers = data.get('headers', {})  # 默认空字典
        # expected = data.get('expected')  # 注意字段名拼写是否正确
        # ignore_keys = data.get('ignore_keys', [])
        # desc = data.get('desc')
        # creator = data.get('creator')
        # created_at = data.get('created_at')
        # method = data.get('method')
        # modifier = data.get('modifier')
        # module = data.get('module')

        # print(f"id:{id}，{type(id)}")
        # print(f"method:{method}，{type(method)}")
        # print(f"url:{url},{type(url)}")
        # print(f"params:{params},{type(params)}")
        # print(f"headers:{headers},{type(headers)}")
        # print(f"expected:{expected},{type(expected)}")
        # print(f"ignore_keys:{ignore_keys},{type(ignore_keys)}")
        # print(f"desc:{desc},{type(desc)}")
        # print(f"creator:{creator},{type(creator)}")
        # print(f"created_at:{created_at},{type(created_at)}")
        # print(f"modifier:{modifier},{type(modifier)}")
        # print(f"module:{module},{type(module)}")

        modifier = data.get('modifier')
        modifier = json.loads(modifier)  # ['userName']


        if not id:
            print("无有效更新字段")
            return resCase(success=False, message='无有效更新字段-id！', code=500)


        # 提取字段并动态构建 SQL
        set_clauses = []  # 存放 SET 子句的片段（如 "method = %s"）
        update_args = []  # 存放对应的参数值

        # 检查并添加每个字段
        # 1. method（字符串类型，非空才更新）
        if 'method' in data and data['method'] is not None and data['method'].strip() != '':
            set_clauses.append("method = %s")
            update_args.append(data['method'])

        # 2. url（字符串类型，非空才更新）
        if 'url' in data and data['url'] is not None and data['url'].strip() != '':
            set_clauses.append("url = %s")
            update_args.append(data['url'])

        # 3. params（字典类型，非空才更新）
        if 'params' in data and data['params']:  # 过滤空字典
            set_clauses.append("params = %s")
            update_args.append(data['params'])  # 转为 JSON 字符串

        # 4. headers（字典类型，非空才更新）
        if 'headers' in data and data['headers']:
            set_clauses.append("headers = %s")
            update_args.append(data['headers'])

        # 5. expected（允许 None，但字段存在才更新）
        if 'expected' in data:  # 显式传递字段时更新，包括 None
            set_clauses.append("expected = %s")
            update_args.append(data['expected'])




        # 6. ignore_keys（列表类型，非空才更新）
        if 'ignore_keys' in data and data['ignore_keys']:
            set_clauses.append("ignore_keys = %s")
            update_args.append(data['ignore_keys'])
        # 7. desc（字符串，非空才更新）
        if 'desc' in data and data['desc'] is not None:
            set_clauses.append("`desc` = %s")  # 关键：用反引号包裹字段名
            update_args.append(data['desc'])

        # 8. 模块（字符串，非空才更新）
        if 'module' in data and data['module'] is not None:
            set_clauses.append("`module` = %s")  # 关键：用反引号包裹字段名
            update_args.append(data['module'])

        # 9. 环境（字符串，非空才更新）
        if 'env' in data and data['env'] is not None:
            set_clauses.append("`env` = %s")  # 关键：用反引号包裹字段名
            update_args.append(data['env'])

        # 10. 更新时间（字符串，非空才更新）

        set_clauses.append("`updated_at` = %s")  # 关键：用反引号包裹字段名
        update_args.append(get_current_time_str())

        # expected

        # 11. 预期结果（字典类型，非空才更新）
        if 'expected' in data and data['expected'] is not None:
            set_clauses.append("expected = %s")
            update_args.append(data['expected'])

        # 12. 修改人（string，非空才更新）
        if 'modifier' in data and data['modifier'] is not None:
            set_clauses.append("modifier = %s")
            update_args.append(modifier['userName'])

        # 13. 状态（string，非空才更新）
        if 'is_deleted' in data and data['is_deleted'] is not None:
            set_clauses.append("is_deleted = %s")
            update_args.append(data['is_deleted'])


        #更新时间

        # set_clauses.append("updated_at = %s")
        # update_args.append(json.dumps(updated_at))

        # 如果没有可更新的字段，直接返回
        if not set_clauses:
            print("无有效更新字段")
            return resCase(success=False, message='无有效更新字段！', code=500)

        # 组合完整 SQL（假设 WHERE 条件为 id=目标值）
        sql = f"UPDATE test_cases SET {', '.join(set_clauses)} WHERE id = %s"
        update_args.append(id)  # 添加 WHERE 条件参数

        print(f"sql:{sql}")
        print(f"update_args:{update_args}")
        # 调用更新函数
        try:
            result = update_one(sql, tuple(update_args))

            return resCase(data=result, message='更新成功！')
        except pymysql.MySQLError as e:
            return resCase(success=False, message=f'更新失败， {e}！', code=500)


    except KeyError as e:
        # 处理字段缺失错误

        return res(message=f"修改用例失败，数据缺少必要字段: {str(e)}", success=False, code=500)

    except Exception as e:
        # 捕获其他异常（如接口请求失败）

        return res(message=f"服务器内部错误-修改用例: {str(e)}", success=False, code=500)


#编辑已有用例的状态
@case_bp.route('/changeCaseStatus', methods=['GET', 'POST'])
# @jwt_required()
def change_Case_Status():
    data = request.get_json()

    modifier = data.get('modifier')
    modifier = json.loads(modifier) #['userName']

    if not data:
        # 返回明确的错误信息，避免引用未定义的 result
        # 400 Bad Request
        return res(message="请求数据为空", success=False, code=400)

    try:
        id = data.get('id')

        if not id:

            return resCase(success=False, message='无有效更新字段-id！', code=500)

        # 提取字段并动态构建 SQL
        set_clauses = []  # 存放 SET 子句的片段（如 "method = %s"）
        update_args = []  # 存放对应的参数值
        status = data.get('status')



        # 如果没有可更新的字段，直接返回
        if not status:

            return resCase(success=False, message='无有效更新字段！', code=500)

        update_args.append(status)
        # 组合完整 SQL（假设 WHERE 条件为 id=目标值）
        sql = "UPDATE test_cases SET is_deleted = %s,updated_at = %s,modifier = %s WHERE id = %s"

        update_args.append(get_current_time_str())

        update_args.append(modifier['userName'])
        update_args.append(id)  # 添加 WHERE 条件参数



        # 调用更新函数
        try:
            result = update_one(sql, tuple(update_args))

            return resCase(data=result, message='更新成功！')
        except pymysql.MySQLError as e:
            return resCase(success=False, message=f'更新失败， {e}！', code=500)



    except KeyError as e:

        # 处理字段缺失错误

        return res(message=f"修改用例状态失败，数据缺少必要字段: {str(e)}", success=False, code=500)


    except Exception as e:

        # 捕获其他异常（如接口请求失败）

        return res(message=f"服务器内部错误-修改用例状态: {str(e)}", success=False, code=500)


# 新增用例的状态
@case_bp.route('/addCase', methods=['POST'])
# @jwt_required()
def add_Case():
    data = request.get_json()
    if not data:
        # 返回明确的错误信息，避免引用未定义的 result
        # 400 Bad Request
        return res(message="请求数据为空", success=False, code=400)

    try:
        # 打印接收到的数据（调试用）
        # print("Received data:", data)

        # 提取必要字段（建议增加字段存在性校验）
        id = generate_caseid()
        method = data.get('method')
        url = data.get('url')
        params = data.get('params', {})  # 默认空字典
        headers = data.get('headers', {})  # 默认空字典
        expected = data.get('expected')  # 注意字段名拼写是否正确
        ignore_keys = data.get('ignore_keys', [])
        desc = data.get('desc')
        creators = data.get('creator')
        created_at = data.get('created_at')
        method = data.get('method')
        modifier = data.get('modifier')
        module = data.get('module')
        is_deleted = data.get('is_deleted')

        print(f"id:{id}，{type(id)}")
        print(f"method:{method}，{type(method)}")
        print(f"url:{url},{type(url)}")
        print(f"params:{params},{type(params)}")
        print(f"headers:{headers},{type(headers)}")
        print(f"expected:{expected},{type(expected)}")
        print(f"ignore_keys:{ignore_keys},{type(ignore_keys)}")
        print(f"desc:{desc},{type(desc)}")
        print(f"creator:{creators},{type(creators)}")
        print(f"created_at:{created_at},{type(created_at)}")
        print(f"modifier:{modifier},{type(modifier)}")
        print(f"module:{module},{type(module)}")
        print(f"is_deleted:{is_deleted},{type(is_deleted)}")

        if not id:
            print("无有效更新字段")
            return resCase(success=False, message='无有效更新字段-id！', code=500)

        # 提取字段并动态构建 SQL
        set_clauses = []  # 存放 SET 子句的片段（如 "method = %s"）
        update_args = []  # 存放对应的参数值
        set_values = []
        # set_clauses.append("`id`")
        # set_values.append("%s")
        # update_args.append(id)  # 添加 WHERE 条件参数
        set_clauses.append("`id`")
        set_values.append("%s")
        update_args.append(id)

        # 检查并添加每个字段
        # 1. method（字符串类型，非空才更新）
        if 'method' in data and data['method'] is not None and data['method'].strip() != '':
            set_clauses.append("`method`")
            set_values.append("%s")
            update_args.append(data['method'])

        # 2. url（字符串类型，非空才更新）
        if 'url' in data and data['url'] is not None and data['url'].strip() != '':
            set_clauses.append("`url`")
            set_values.append("%s")
            update_args.append(data['url'])

        # 3. params（字典类型，非空才更新）
        if 'params' in data and data['params']:  # 过滤空字典
            set_clauses.append("`params`")
            set_values.append("%s")
            update_args.append(data['params'])  # 转为 JSON 字符串

        # 4. headers（字典类型，非空才更新）
        if 'headers' in data and data['headers']:
            set_clauses.append("`headers`")
            set_values.append("%s")
            update_args.append(data['headers'])

        # 5. expected（允许 None，但字段存在才更新）
        if 'expected' in data:  # 显式传递字段时更新，包括 None
            set_clauses.append("`expected`")
            set_values.append("%s")
            update_args.append(data['expected'])

        # 6. ignore_keys（列表类型，非空才更新）
        if 'ignore_keys' in data and data['ignore_keys']:
            set_clauses.append("`ignore_keys`")
            set_values.append("%s")
            update_args.append(data['ignore_keys'])
        # 7. desc（字符串，非空才更新）
        if 'desc' in data and data['desc'] is not None:
            set_clauses.append("`desc`")  # 关键：用反引号包裹字段名
            set_values.append("%s")
            update_args.append(data['desc'])

        # 8. 模块（字符串，非空才更新）
        if 'module' in data and data['module'] is not None:
            set_clauses.append("`module`")  # 关键：用反引号包裹字段名
            set_values.append("%s")
            update_args.append(data['module'])

        # 9. 环境（字符串，非空才更新）
        if 'env' in data and data['env'] is not None:
            set_clauses.append("`env`")  # 关键：用反引号包裹字段名
            set_values.append("%s")
            update_args.append(data['env'])

        set_clauses.append("`creator`")  # 关键：用反引号包裹字段名
        set_values.append("%s")
        creators = json.loads(creators)
        update_args.append(creators['userName'])

        set_clauses.append("`modifier`")  # 关键：用反引号包裹字段名
        set_values.append("%s")
        update_args.append(creators['userName'])

        # 10. 更新时间（字符串，非空才更新）/创建时间

        set_clauses.append("`updated_at`")  # 关键：用反引号包裹字段名
        set_values.append("%s")
        update_args.append(get_current_time_str())

        set_clauses.append("`created_at`")  # 关键：用反引号包裹字段名
        set_values.append("%s")
        update_args.append(get_current_time_str())

        set_clauses.append("`is_deleted`")  # 关键：用反引号包裹字段名
        set_values.append("%s")
        update_args.append(data['is_deleted'])


        # 更新时间

        # set_clauses.append("updated_at = %s")
        # update_args.append(json.dumps(updated_at))

        # 如果没有可更新的字段，直接返回
        if not set_clauses:
            print("无有效更新字段")
            return resCase(success=False, message='无有效更新字段！', code=500)

        # 组合完整 SQL（假设 WHERE 条件为 id=目标值）
        sql = f"INSERT INTO test_cases ( {', '.join(set_clauses)} ) VALUES ({', '.join(set_values)})"


        # print(f"sql:{sql}")
        # print(f"update_args:{update_args}")
        # 调用添加函数
        try:
            result = insert_one_pk(sql, update_args)

            # print(f'result:{result}')

            return resCase(data=result, message='新增成功！')
        except pymysql.MySQLError as e:
            return resCase(success=False, message=f'新增失败， {e}！', code=500)


    except KeyError as e:
        # 处理字段缺失错误

        return res(message=f"新增用例失败，数据缺少必要字段: {str(e)}", success=False, code=500)

    except Exception as e:
        # 捕获其他异常（如接口请求失败）

        return res(message=f"服务器内部错误-新增用例: {str(e)}", success=False, code=500)
