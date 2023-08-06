# Created by Q-ays.
# whosqays@gmail.com

# install sqlalchemy before use

# postgres tools

from sqlalchemy.exc import SQLAlchemyError, TimeoutError
import traceback
import json


def session_exception(session, is_raise=True):
    def wrapper(func):

        def catch(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except SQLAlchemyError as e:
                # print(e)
                print('~~~~~~~~~~~~~~~~session error~~~~~~~~~~~~~~~~~~')
                traceback.print_exc()
                if not isinstance(e, TimeoutError):
                    session.rollback()
                if is_raise:
                    raise e

        return catch

    return wrapper


def to_dict(self):
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


def str2js(ls):
    """
    json字符转字典
    :param ls:
    :return:
    """
    if isinstance(ls, list):
        ls0 = list()

        try:
            for l in ls:
                ls0.append(json.loads(l))

            return ls0
        except:
            pass

    return ls


def detect_filed(o, *args):
    """
    特定字段字符转json
    :param o:
    :param args:
    :return:
    """
    for arg in args:
        n = o.get(arg)
        if n:
            o[arg] = str2js(n)

    return o


def o2d(obj):
    """
    把对象(支持单个对象、list、set)转换成字典
    针对postgres数据库
    :param obj: obj, list, set
    :return:
    """

    if isinstance(obj, dict) or (not obj):
        return obj

    is_list = isinstance(obj, list)
    is_set = isinstance(obj, set)

    if is_list or is_set:
        obj_arr = []

        for o in obj:
            if o:
                if isinstance(o, dict):
                    n = detect_filed(o, 'roles', 'org')
                else:
                    n = detect_filed(o.to_dict(), 'roles', 'org')

                obj_arr.append(n)
        return obj_arr
    else:
        return detect_filed(obj.to_dict(), 'roles', 'org')


def repo_ref(session0):
    """
    基于postgres 数据库增删改查的公共类
    :param session0:
    :return:
    """

    class RepoBase:
        def __init__(self, Model=None):
            self.session = session0
            self.Model = Model

        def add(self, **data):
            try:
                model0 = self.Model(**data)
                self.session.add(model0)
                self.session.commit()
                return model0
            except Exception as e:
                self.session.rollback()
                raise e

        def delete(self, did=None, **kwargs):
            did = did if did else kwargs.get('id')
            if did:
                repo = self.session.query(self.Model).get(did)

                self.session.delete(repo)
                self.session.commit()

                return repo
            else:
                if kwargs:
                    repos = self.session.query(self.Model).filter_by(**kwargs)
                    repos_r = repos.all()
                    repos_d = repos.delete()

                    self.session.commit()

                    return repos_r
            raise Exception('未传参数，删除规则')

        def update(self, did=None, **data):

            did = did if did else data.get('id')

            if not did:
                raise Exception('更新的数据没得id，不晓得更新哪条')

            model0 = self.get(did)

            columns = model0.__table__.columns

            for col in columns:
                name = col.name
                value = data.get(name, None)

                if value is not None and not col.primary_key:
                    setattr(model0, name, value)

            # 统一修改密码
            if data.get('password'):
                model0.password = data.get('password')

            self.session.add(model0)
            self.session.commit()

            return model0

        def get(self, did=None, _fuzzy=None, _sort=None, _slice=None, **kwargs):
            repos = self.session.query(self.Model)

            if did:
                if isinstance(did, list):
                    repos = repos.filter(self.Model.id.in_(did))
                else:
                    repos = repos.get(did)

                    # self.session.close()
                    self.session.commit()

                    return repos
            elif kwargs:
                if _fuzzy:
                    for (k, v) in kwargs.items():
                        if isinstance(v, list):
                            if len(v) == 2:
                                repos = repos.filter(getattr(self.Model, k).between(*v))
                        else:
                            repos = repos.filter(getattr(self.Model, k).like('%' + v + '%'))
                else:
                    repos = repos.filter_by(**kwargs)
            else:
                ...

            if _sort:
                if _sort.startswith('-'):
                    repos = repos.order_by(getattr(self.Model, _sort[1:]).desc())
                else:
                    repos = repos.order_by(getattr(self.Model, _sort))

            if _slice:
                repos = repos.slice(*_slice)

            repos = repos.all()
            # self.session.close()
            self.session.commit()

            return repos

        def page(self, did=None, _fuzzy=None, _sort=None, _slice=None, **kwargs):
            """
            paginate and return count total and current slice
            :param did:
            :param _fuzzy:
            :param _sort:
            :param _slice:
            :param kwargs:
            :return:
            """

            repos = self.session.query(self.Model)

            if did:
                if isinstance(did, list):
                    repos = repos.filter(self.Model.id.in_(did))
                else:
                    repos = repos.get(did)

                    # self.session.close()
                    self.session.commit()

                    return repos
            elif kwargs:
                if _fuzzy:
                    for (k, v) in kwargs.items():
                        if isinstance(v, list):
                            if len(v) == 2:
                                repos = repos.filter(getattr(self.Model, k).between(*v))
                        else:
                            repos = repos.filter(getattr(self.Model, k).like('%' + v + '%'))
                else:
                    repos = repos.filter_by(**kwargs)
            else:
                ...

            total = repos.count()

            if _sort:
                if _sort.startswith('-'):
                    repos = repos.order_by(getattr(self.Model, _sort[1:]).desc())
                else:
                    repos = repos.order_by(getattr(self.Model, _sort))

            if _slice:
                repos = repos.slice(*_slice)

            repos = repos.all()
            # self.session.close()
            self.session.commit()

            return {'total': total, 'data': o2d(repos), 'page': _slice}

        def create_view(self, sql_create_view):
            '''
            创建视图函数（视图创建使用后便删除）
            如要查询用户创建的组织信息和用户信息
            select a.account, a.username, row_to_json(o) as org
            from public.user as a, public.organization as o
            where o.owner=a.id
            :param sql_create_view:
            :return: 视图表数据
            '''
            create_view = "create view tzxdview as {}".format(sql_create_view)
            sql_2 = "select * from tzxdview"
            try:
                self.session.execute(create_view)
            except:
                self.session.close()
                raise Exception('语句执行错误！')

            res = self.session.execute(sql_2)
            self.session.execute("drop view tzxdview")
            self.session.close()
            res = [dict(r) for r in res]
            return res

    return RepoBase
