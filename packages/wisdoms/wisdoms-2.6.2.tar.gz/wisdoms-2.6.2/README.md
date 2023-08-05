[TOC]

# 通用库

## 用法
1. 此库作为git项目管理，凡是修改完后应及时通知到开发团队
2. 需要使用库中的方法，使用pip install,这时候就可以在项目中引用库中的方法
3. 引用的方法举例：

----------------------------------------------------------

- #### generation - 更新库

_Make sure you have installed setuptools and wheel._

_Important: You must modify the version of the package in setup.py and then delete those folders (build, dist, egg-info)_

> python setup.py sdist bdist_wheel

- #### upload - 上传代码

Install twine before doing this(qays:一只会抓鱼的熊）
> twine upload dist/*

------------------------------------------------------------

- #### install - 安装
> pip install wisdoms

- #### find the latest package of wisdoms - 发现最新版本
> pip list --outdated

- #### upgrade - 升级到最新包
> pip install wisdoms --upgrade --no-cache-dir


## packets usage:

- #### ms.py:

``` python

# 权限验证
from wisdoms.ms import permit, add_uid, add_user

host = {'AMQP_URI': "amqp://guest:guest@localhost"}

auth_ = permit(host)
user_ = add_user(host)
uid_ = add_uid(host)


class A:

    @auth_
    def func_need_auth(self, data):
        """
        1.进入这个方法之前会验证权限，data需带有token
        2.之后的data的数据结构：
        {'uid':用户id, 'full_user':用户全部信息字典类型,'data':前端传来的data,'token':token,'full_org':当前组织, 'user':精简用户信息,'org':精简组织信息}
        :param data:
        :return:
        """
        user = data.get('user')
        data = data.get('data')
        # ...

    @user_
    def func_need_user(self, data):
        """
        1.进入这个方法不需要验证权限，需要token返回用户信息
        2.之后的data的数据结构：
        {'uid':用户id, 'full_user':用户全部信息字典类型,'data':前端传来的data,'token':token,'full_org':当前组织, 'user':精简用户信息,'org':精简组织信息}
        :param data:
        :return:
        """
        user = data.get('user')
        data = data.get('data')
        # ...

    @uid_
    def func_need_uid(self, data):
        """
        1.进入这个方法不需要验证权限，需要token只返回用户id
        2.之后的data的数据结构：{'uid':用户id, 'data':前端传来的data,'token':token}
        :param data:
        :return:
        """
        uid = data.get('uid')
        data = data.get('data')
        # ...

```

- #### config.py

``` python

# 读取yml配置
from wisdoms.config import c

# gains item of YML config
print(c.get('name'))

# transforms class into dict
d = c.to_dict()
print(d['name'])

```

- #### commons package

``` python

# 返回执行后的状态码
from wisdoms.commons import revert, codes, success

def func():
    # do something

    # revert(codes.code) or revert(number)
    # return revert(1)
    return revert(codes.ERROR)

def foo():
    # return revert(code, data, desc)
    return revert(codes.SUCCESS, {'data':'data'},'返回成功描述信息')

def done():
    # simplified revert where success execute
    # return success(data) or success()
    return success()
```

- #### util.py
``` python

# 多个字符串连接成路径
from wisdoms.utils import joint4path

print(joint4path('abc','dac','ccc'))

# $: abc/dac/ccc

# ------------------------------------------------------------------
# 对象转字典
from wisdoms.utils import o2d

o2d(obj)

# ------------------------------------------------------------------
# 捕获异常装饰器
from wisdoms.utils import func_exception

ex = func_exception(codes.WARNING)

@ex
def func():
    pass


# ------------------------------------------------------------------
# 捕获异常类装饰器
from wisdoms.utils import cls_exception

# ex为方法装饰器
xpt_cls = cls_exception(ex)

@xpt_cls
class A:
    name = 'a'

    def __init__(self, param):
        self.desc = param

    def func1(self, param):
        return self.desc + param

    @classmethod
    def func2(cls, param):
        print(cls)
        print('func2', param)
        raise Exception('func2 error')

    @staticmethod
    def func3(param):
        print('func3', param)
        raise Exception('func3 error')

aa = A('param')
# 注意： 该装饰器的静态方法和类方法必须用实例调用
```

- #### ms.py
``` python

# 应用微服务 基类
from wisdoms.ms import ms_base

from xx import ROLES

# ROLES 数据结构
# import json

# defRole = {
#     'role': 'default',
#     'name': '默认角色',
#     'desc': '',
#     'functions': ['user_register', 'user_update', 'user_logoff', 'user_search', 'user_audit', 'user_login',
#                   'user_logout', 'org_register', 'org_update', 'org_dismiss', 'org_search', 'org_audit',
#                   'org_user_list', 'app_register', 'app_update', 'app_delete', 'app_search', 'app_audit',
#                   'user_org_apply', 'user_org_choose', 'user_org_list', 'user_org_audit', 'user_org_update',
#                   'user_org_rid', 'user_app_apply', 'user_app_apply_list', 'user_app_audit', 'user_app_update',
#                   'user_app_rid', 'user_app_router'],
#     'router': {}
# }

# ROLES = list()

# ROLES.append(json.dumps(defRole))



# 不需要的不写
MsBase = ms_base(MS_HOST, name='XX应用', roles=ROLES, types='free',entrance='/xx/index')


class A(MsBase):
    pass

# -----------------------------------------------
from wisdoms.ms import closure_crf

crf = closure_crf(config('ms_host'))
```

- #### pg_db.py
``` python

from wisdoms.pg_db import session_exception

se = session_exception(session)

@se
def func():
    # raise exception extend SqlalChemyError
    pass

# ------------------------------------------------------------------
# session 增删改查表基础类，已经实现增删改查通用方法，直接继承就能使用
from wisdoms.db import repo_ref

RepoBase = repo_ref(session)

class FooRepo(RepoBase):
    """
    common add, delete, update, get(include search) function finished
    """
    pass

# Foo is the model of table
foo = FooRepo(Foo)

# you can do follow list
foo.add(name='name', desc='desc',...)
foo.update(id, name = 'rename',desc = 'redesc',...)
foo.delete(id)

foo.get() # return list of all objects
foo.get(id) # return a object
foo.get(name ='name',...) # return list of objects what you search


#-----------------------------------------------------


    
postgresql 使用ARRAYJSON
使用 jsonb 来存储
example: notes = Column(CastingArray())

class CastingArray(ARRAY):

    def bind_expression(self):
        return cast(JSONB, self)

#---------------------------------------------------------

定制PG model 五个基本属性
class BaseModelPG(declarative_base()):
    __abstract__ = True  

    # 定制基本属性
    id = Column(Integer, nullable=False, primary_key=True, unique=True, autoincrement=True, )
    uid = Column(Integer, nullable=False)
    oid = Column(Integer, nullable=False)
    create_time = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    update_time = Column(DateTime, default=datetime.now(), )
    
    
使用例子
class SomeEntity(BaseModelPG):
    name = models.CharField(max_length=1000)
    address = models.CharField(max_length=1000, default='')
    info = models.CharField(max_length=2000, default='')

```


## 如何设计包
- 顶级包：wisdom，代表天智，智慧
- 现阶段的约定：采用一级包的方式
- 不同的功能放在不同的文件（模块）即可做好方法的分类
