from flask import request
from flask_restful import Resource

from app.api.common.utils import res
from app.commen.resopDiff import resp_diff
from app.interfaces.interfaces import interfaces


class TestCase(Resource):

    def post(self):
        data = request.get_json()

        if not data:
            # 返回明确的错误信息，避免引用未定义的 result
            # 400 Bad Request
            return res(message="请求数据为空", success=False, code=400)

        try:
            # 打印接收到的数据（调试用）
            # print("Received data:", data)

            # 提取必要字段（建议增加字段存在性校验）
            method = data.get('method')
            url = data.get('url')
            params = data.get('params', {})  # 默认空字典
            headers = data.get('headers', {})  # 默认空字典
            expected = data.get('expected')  # 注意字段名拼写是否正确
            ignore_keys = data.get('ignore_keys', [])

            print(f"method:{method}，{type(method)}")
            print(f"url:{url},{type(url)}")
            print(f"params:{params},{type(params)}")
            print(f"headers:{headers},{type(headers)}")
            print(f"expected:{expected},{type(expected)}")
            print(f"ignore_keys:{ignore_keys},{type(ignore_keys)}")



            # 调用接口请求,headers和params都必须是dict格式
            resp = interfaces.request(
                method=method,
                url=url,
                headers=headers,
                params=params
            )

            print(f"resp:{resp}")
            print(f"resp.txt:{resp.text},{type(resp.text)}")

            # 确保获取响应文本内容
            resp_text = resp.text


            # # 调试输出响应内容
            # print("Response text:", resp_text)

            # 对比预期结果与实际响应
            # 假设 resp_diff 返回可序列化的字典（需确保实现正确）
            result = resp_diff(expected, resp_text, ignore_keys)

            # print(f"result:{result}")

            # 构建返回结果
            if not result:  # 等价于 result == {}

                return res(data=result, message="接口对比一致，测试通过！", success=True, code=200)
            else:

                return res(data=result, message="接口对比不一致，测试不通过！", success=False, code=200)

        except KeyError as e:
            # 处理字段缺失错误

            return res(message=f"请求数据缺少必要字段: {str(e)}", success=False, code=500)

        except Exception as e:
            # 捕获其他异常（如接口请求失败）

            return res(message=f"服务器内部错误: {str(e)}", success=False, code=500)
