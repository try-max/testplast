import requests


class Interfaces:
    def __init__(self):
        """session管理器"""
        self.session = requests.session()

    def request(self, method, url, params=None, headers=None, **kwargs):
        # 根据请求方法自适应传递参数
        if method.upper() in ['GET', 'DELETE']:
            # GET 请求使用 params 传递查询参数
            response = self.session.request(method, url, params=params, headers=headers, **kwargs)
        elif method.upper() in ['POST', 'PUT', 'PATCH']:
            # POST、PUT、PATCH、DELETE 请求使用 data 或 json 传递请求体数据
            response = self.session.request(method, url, data=params, headers=headers, **kwargs)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        return response


    def close_session(self):
        """关闭session"""
        self.session.close()



interfaces = Interfaces()