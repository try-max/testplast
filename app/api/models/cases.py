from ..common.utils import format_datetime_to_json, res
from ..models import db
from datetime import datetime


class CasesModel(db.Model):
    """
     用例表
    """
    __tablename__ = 'test_cases'

    # case id
    id = db.Column(db.Integer(), primary_key=True, nullable=False, autoincrement=True, comment='用例唯一ID')
    # 环境
    env = db.Column(db.String(50), nullable=False, default='', comment='环境：RC、Stage、Prod')
    # 模块
    module = db.Column(db.String(50), nullable=False, default='', comment='模块：stat、user、noah')
    # 创建人
    creator = db.Column(db.String(50), nullable=False, comment='创建人')
    # 创建时间
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now, comment='创建时间')
    # 修改人
    modifier = db.Column(db.String(50), nullable=False, comment='最后一次修改人')
    # 修改时间
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    # 创建时间
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now, comment='创建时间')
    # 更新时间
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    # 请求信息
    method = db.Column(db.Enum('GET', 'POST', 'PUT', 'DELETE', 'PATCH', name='http_method'),
                       nullable=False, comment='请求方法')
    url = db.Column(db.String(255), nullable=False, comment='接口URL')
    headers = db.Column(db.JSON, comment='请求头（JSON格式）')
    params = db.Column(db.JSON, comment='请求参数（JSON格式）')
    # 结果校验
    expected = db.Column(db.JSON, nullable=False, comment='预期结果（JSON格式）')
    ignored_fields = db.Column(db.JSON, comment='忽略校验字段（JSON数组）')
    # 控制标记
    is_deleted = db.Column(db.Boolean, default=0, comment='软删除标记')
    skip_execution = db.Column(db.Boolean, default=False, comment='是否跳过执行')

    # 新增用例
    @classmethod
    def create_case(env, module, creator, modifier, method, url, headers, params, expected, ignored_fields=None):
        """
        创建新用例
        """
        new_case = CasesModel(
            env=env,
            module=module,
            creator=creator,
            modifier=modifier,
            method=method,
            url=url,
            headers=headers,
            params=params,
            expected=expected,
            ignored_fields=ignored_fields or []
        )
        db.session.add(new_case)
        try:
            db.session.commit()
            return new_case
        except Exception as e:
            db.session.rollback()
            raise e

    # 查询用例
    @classmethod
    def get_all_cases(cls):
        """
        获取所有未删除的用例
        """
        try:
            cases = CasesModel.query.filter_by(is_deleted=0).all()

            return [case.to_dict() for case in cases]  # 假设有 to_dict() 方法
        except:
            return res(success=False, message='服务器繁忙！', code=500)


    # 查询单个用例
    @classmethod
    def get_case_by_one(env=None, module=None, creator=None, modifier=None, method=None, url=None):
        """
            根据环境和模块等其他组合过滤用例
        """
        query = CasesModel.query.filter_by(is_deleted=0)
        if creator:
            query = query.filter_by(creator=creator)
        if env:
            query = query.filter_by(env=env)
        if module:
            query = query.filter_by(module=module)
        if modifier:
            query = query.filter_by(modifier=modifier)
        if method:
            query = query.filter_by(method=method)
        if url:
            query = query.filter_by(method=url)
        return [case.to_dict() for case in query.all()]

    # 更新用例
    @classmethod
    def update_case(case_id, **kwargs):
        """
        更新用例信息
        """
        case = CasesModel.query.get(case_id)
        if not case:
            return None

        updatable_fields = ['env', 'module', 'method', 'url', 'headers', 'params', 'expected', 'ignored_fields',
                            'modifier']
        for key, value in kwargs.items():
            if key in updatable_fields:
                setattr(case, key, value)
        case.updated_at = datetime.now()  # 手动触发更新时间（确保 onupdate 生效）

        try:
            db.session.commit()
            return case.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e

    # 删除用例
    @classmethod
    def soft_delete_case(case_id, modifier):
        """
        软删除：标记 is_deleted 为 1
        """
        case = CasesModel.query.get(case_id)
        if not case:
            return False

        case.is_deleted = 1
        case.modifier = modifier  # 记录操作人
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False

    # 序列化方法
    @classmethod
    def to_dict(cls):
        return {
            "id": cls.id,
            "env": cls.env,
            "module": cls.module,
            "creator": cls.creator,
            "modifier": cls.modifier,
            "created_at": format_datetime_to_json(cls.created_at),
            "updated_at": format_datetime_to_json(cls.updated_at),
            "method": cls.method,
            "url": cls.url,
            "headers": cls.headers,
            "params": cls.params,
            "expected": cls.expected,
            "ignored_fields": cls.ignored_fields,
            "is_deleted": cls.is_deleted,
            "skip_execution": cls.skip_execution
        }

# print(CasesModel.get_all_cases())