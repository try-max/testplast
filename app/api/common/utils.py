# 公共 response 方法
def res(data=None, message='OK', success=True, code=200):
    return {
        'success': success,
        'message': message,
        'data': data
     }, code


#接口信息列表
def resCase(data=None, message='OK', success=True, code=200):
    return {
        'success': success,
        'message': message,
        'data': {
            'list': data
        },
     }, code


# datetime 转换格式
def format_datetime_to_json(datetime, format='%Y-%m-%d %H:%M:%S'):
    return datetime.strftime(format)

