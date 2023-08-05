# Created by Q-ays.
# whosqays@gmail.com


from enum import Enum, unique, IntEnum


@unique
class Code(Enum):
    ERROR = -1, '错误'
    MS_ERROR = -2, '微服务错误'
    DATABASE_ERROR = -3, '数据库错误'
    TIMEOUT = -4, '超时'
    USER_ERROR = -5, '用户出错',
    TOKEN_ERROR = -6, 'token验证出错'

    SUCCESS = 1, '成功'
    WARNING = 99, '警告'
    UNKNOWN = 0, '未知'

    def __init__(self, code, msg):
        self._code = code
        self.msg = msg

    @property
    def get_code(self):
        return self._code

    @property
    def get_msg(self):
        return self.msg


class WisdomErrorException(Exception):
    """
    顶层异常类
    """

    def __init__(self, desc=None, code=0, code_enum=Code.UNKNOWN):
        self.codeEnum = code_enum
        self.code = code
        self.desc = desc

    def gene_code(self):
        if self.__class__.__name__ == 'WisdomErrorException':
            return self.assemble_error_code(0, self.my_code)
        parent = self.__class__.mro()[1]()
        return self.assemble_error_code(parent.my_code, self.my_code)

    @staticmethod
    def assemble_error_code(parent: int, child: int):
        return -(10000 + abs(parent) * 100 + abs(child))

    @property
    def my_desc(self):
        if hasattr(self, 'desc'):
            return self.desc if self.desc else (
                '无描述信息-none described msg' if not hasattr(self, 'codeEnum') else self.codeEnum.get_msg)

    @property
    def my_msg(self):
        return '无内容-null of contents' if not hasattr(self, 'codeEnum') else self.codeEnum.get_msg

    @property
    def my_data(self):
        return None if not hasattr(self, 'data') else self.data

    @property
    def my_code(self):
        if hasattr(self, 'codeEnum'):
            return self.codeEnum.get_code if self.codeEnum else 0
        if hasattr(self, 'code'):
            return self.code if self.code else 0
        return 0

    def revert(self):
        return {"code": self.gene_code(), 'desc': self.my_desc, 'msg': self.my_msg, 'data': self.my_data}

    def __call__(self):
        return {"code": self.gene_code(), 'desc': self.my_desc, 'msg': self.my_msg, 'data': self.my_data}


class CommonException(WisdomErrorException):
    """
    公用报错异常类
    """

    def __init__(self, desc=None, code=-1, data=None, code_enum=Code.ERROR):
        self.desc = desc
        self.code = code
        self.data = data
        self.codeEnum = code_enum


class DbException(WisdomErrorException):
    """
    数据库异常父类
    """

    def __init__(self, desc=None, data=None, code_enum=Code.DATABASE_ERROR):
        self.data = data
        self.desc = desc
        self.codeEnum = code_enum


class UserException(WisdomErrorException):
    """
    用户操作异常父类
    """

    def __init__(self, desc=None, data=None, code_enum=Code.USER_ERROR):
        self.data = data
        self.desc = desc
        self.codeEnum = code_enum


class TokenException(UserException):
    """
    token 验证异常
    """

    def __init__(self, desc=None, data=None, code_enum=Code.TOKEN_ERROR):
        self.data = data
        self.desc = desc
        self.codeEnum = code_enum


class MsException(WisdomErrorException):
    """
    微服务异常父类
    """

    def __init__(self, desc=None, data=None, code_enum=Code.MS_ERROR):
        self.data = data
        self.desc = desc
        self.codeEnum = code_enum


class TimeoutException(WisdomErrorException):
    """
    超时异常父类
    """

    def __init__(self, desc=None, data=None, code_enum=Code.TIMEOUT):
        self.data = data
        self.desc = desc
        self.codeEnum = code_enum


class PostgresException(DbException):
    def __init__(self, desc='pg数据库错误', code=1):
        self.desc = desc
        self.code = code


class EsException(DbException):
    pass


if __name__ == '__main__':
    # CommonException('djfidso').gene_code()
    def example():
        return UserException('djfidso')
    example()
    
    # try:
    #     # raise WisdomErrorException()
    #     raise UserException()

    # except WisdomErrorException as e:
    #     print(e.revert())
