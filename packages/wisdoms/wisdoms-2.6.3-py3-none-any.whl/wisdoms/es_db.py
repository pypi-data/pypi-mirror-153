# Created by Q-ays.
# whosqays@gmail.com

# install elasticsearch_dsl before use

# elastic-search tools

from datetime import datetime

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Q, Search


def inner_o2d_filter(o, date_filter=True):
    if date_filter:
        for k in o:
            if isinstance(o[k], dict):
                inner_o2d_filter(o[k])
            if isinstance(o[k], datetime):
                o[k] = o[k].strftime("%Y-%m-%d %H:%M:%S")


def o2d(obj, date_filter=True):
    is_arr = isinstance(obj, list)
    is_set = isinstance(obj, set)

    if is_set or is_arr:
        res = []
        for o in obj:
            if not isinstance(o, dict):
                d0 = o.to_dict(include_meta=True)
                d1 = d0.get('_source')
                d1['id'] = d0.get('_id')
                inner_o2d_filter(d1, date_filter=date_filter)
                res.append(d1)
            else:
                if o.get('_source'):
                    d0 = o.get('_source')
                    d0['id'] = o.get('_id')
                    inner_o2d_filter(d0, date_filter=date_filter)
                    res.append(d0)
                else:
                    inner_o2d_filter(o, date_filter=date_filter)
                    res.append(o)

        return res

    if not isinstance(obj, dict):
        d0 = obj.to_dict(include_meta=True)
        d1 = d0.get('_source')
        d1['id'] = d0.get('_id')
        inner_o2d_filter(d1, date_filter=date_filter)
        return d1
    else:
        if obj.get('data'):
            data = obj.get('data')
            obj['data'] = o2d(data)

        return obj


def str2arr(value, char=','):
    """分离字符串通过特殊字符"""

    if not value or not isinstance(value, str):
        return None

    sort_list = value.split(char)
    return list(filter(lambda x: x.strip(), sort_list))


def paging(s, index: str, searches: dict, page=(0, 50), sort: str = None, types: str = None, **kwargs):
    """
    搜索并带分页功能
    :param s: 搜索对象
    :param index: index名称
    :param searches: 搜索字典
    :param page: (10,20) {"from": 10, "to": 20}
    :param sort: 排序
    :param types: 搜索类型 term, match 默认wildcard模糊搜索
    :param kwargs:
    :return:
    """

    # s = Search(using=self.es, index=index)
    s = s.extra(track_total_hits=True)
    keyword = kwargs.get('keyword') if isinstance(kwargs.get('keyword'), str) else 'keyword'
    if keyword:
        keyword = '.' + keyword

    detail = kwargs.get('detail', {})
    # 搜索查询
    try:
        # 查询字段在es里面是否存在
        exists_fields_and = detail.get('exists_fields_and_', None)
        exists_fields_or = detail.get('exists_fields_or_', None)
        print(detail)

        if isinstance(exists_fields_and, list):
            q = Q()
            for field in exists_fields_and:
                q = q & Q('exists', field=field)

            s = s.query(q)

        if isinstance(exists_fields_or, list):
            q = None
            for field in exists_fields_or:
                if q:
                    q = q | Q('exists', field=field)
                else:
                    q = Q('exists', field=field)

            s = s.query(q)
    except Exception as e:
        print(e)
    # 搜索查询
    if searches:
        for key, value in searches.items():

            types0 = types
            keyword0 = keyword
            reverse0 = False
            exists0 = None

            try:
                # 获取detail里面字段查询限制
                extra_limit = detail.get(key)
                if isinstance(extra_limit, dict):
                    types0 = extra_limit.get('types', types)
                    keyword0 = extra_limit.get('keyword', keyword)
                    reverse0 = extra_limit.get('reverse', False)
                    exists0 = extra_limit.get('exists', None)
                    if keyword0:
                        keyword0 = keyword0 if keyword0.startswith('.') else '.' + keyword0
            except Exception as e:
                print(e)

            # 限制查询字段是否存在
            if exists0 == 'must':
                s = s.query('exists', field=key)
            if exists0 == 'not':
                q = ~Q('exists', field=key)
                s = s.query(q)

            if isinstance(value, dict):
                # nested 对象查询
                q = Q()
                for k, v in value.items():
                    q = q & Q('match', **{str(key) + '.' + k: v})
                s = s.query('nested', path=key, query=q)
            elif isinstance(value, list):
                if types0 in ['terms']:
                    # 范围查询
                    s = s.query(types0, **{key + keyword0: value})
                elif types0 in ['term', 'match']:
                    # 数组and查询
                    for v in value:
                        s = s.query(types0, **{key + keyword0: v})
                else:
                    s = s.query('range', **{key: {'gte': value[0], 'lte': value[1]}})
            else:
                if reverse0:
                    # 取反查询
                    q = ~Q(types0 or 'match', **{key + keyword0: value})
                    s = s.query(q)
                else:
                    if types0 in ['term', 'match']:
                        s = s.filter(types0, **{key + keyword0: value})
                    else:
                        s = s.filter('wildcard', **{key + keyword0: '*' + value + '*'})

    # 处理排序
    sort_list = str2arr(sort)
    if sort_list:
        s = s.sort(*sort_list)  # 排序

    # 分页处理
    page_slice = None
    if (isinstance(page, list) or isinstance(page, tuple)) and len(page) == 2:
        page_slice = slice(page[0], page[1])
        s = s[page_slice]
        func = s.execute
    else:
        func = s.scan

    print('Execute Search Dict:', s.to_dict())

    # 获取结果
    data = {}
    try:
        res = func()
    except Exception as e:
        # 捕捉异常，触发可以处理的异常 `wisdoms 异常`
        # raise
        pass
    else:
        result = [{'id': o.meta.id, **o.to_dict()} for o in res]
        if page_slice:
            data['data'] = result
            data['loc'] = page_slice.start
            data['to'] = page_slice.stop
            data['total'] = res.hits.total.value if hasattr(res.hits.total, 'value') else res.hits.total
        else:
            data = result

    return data


class BaseRepo:
    """
    基于es数据库增删改查的公共类
    """

    def __init__(self, ModelType):
        self.Model = ModelType
        self.index = ModelType.Index.name

    def add(self, data: dict()):
        if 'id' in data.keys():
            del data['id']
        model = self.Model(**data)
        model.save(refresh=True)
        return model

    def delete(self, did=None):
        if did:
            res = self.Model.get(did)
            res.delete()
            return res

    def update(self, did, data):
        model = self.Model.get(did)
        for key in data:
            if hasattr(model, key):
                setattr(model, key, data[key])
        model.save(refresh=True)
        return model

    def get(self, did=None, p=None, **kwargs):
        """
        查询对象字段时，参数为对象
        :param did:
        :param p:
        :param kwargs:
        :return:
        """
        if did:
            if isinstance(did, list):
                obj = self.Model.mget(did)
            else:
                obj = self.Model.get(did)
        else:
            s = self.Model.search()
            s = s.extra(track_total_hits=True)
            for key in kwargs:
                if isinstance(kwargs[key], dict):
                    s = s.query('nested', path=key, query=Q('match', **{str(key) + '.id': kwargs[key].get('id')}))
                else:
                    s = s.query('match', **{key: kwargs[key]})

            if isinstance(p, list) or isinstance(p, tuple):
                s = s[p[0]:p[1]]
                res = s.execute()
            else:
                res = s.scan()

            obj = []
            for o in res:
                obj.append(o)

        return obj

    def _fetch_search_model(self):
        return self.Model.search()

    def query_model(self, querys, p=None):
        """
        [{types:'term',data:{filed.keyword:'xxx'}},{types:'range',data:{field:{lte:xx,gte:xx}}}]
        :param querys:
        :param p:
        :return:
        """

        s = self._fetch_search_model()

        if not isinstance(querys, list):
            querys = [querys]

        for query in querys:
            print(query)
            q = Q(query.get('types') or 'term', **query.get('data'))
            s = s.query(q)

        if isinstance(p, list) or isinstance(p, tuple):
            s = s[p[0]:p[1]]
            res = s.execute()
        else:
            res = s.scan()

        return [{"id": o.meta.id, **o.to_dict()} for o in res]

    def paging(self, searches: dict, page=(0, 50), sort: str = None, types: str = None, **kwargs):
        """
        搜索并带分页功能
        :param searches: 搜索字典
        :param page: (10,20) {"from": 10, "to": 20}
        :param sort: 排序
        :param types: 搜索类型 term, match 默认wildcard模糊搜索
        :param kwargs:
        :return:
        """

        s = self.Model.search()
        s = s.extra(track_total_hits=True)
        keyword = kwargs.get('keyword') if isinstance(kwargs.get('keyword'), str) else 'keyword'
        if keyword:
            keyword = '.' + keyword

        # 搜索查询
        if searches:
            for key, value in searches.items():
                if isinstance(value, dict):
                    # nested 对象查询
                    q = Q()
                    for k, v in value.items():
                        q = q & Q('match', **{str(key) + '.' + k: v})
                    s = s.query('nested', path=key, query=q)
                elif isinstance(value, list):
                    # 范围查询
                    s = s.query('range', **{key: {'gte': value[0], 'lte': value[1]}})
                else:
                    if types in ['term', 'match']:
                        s = s.filter(types, **{key + keyword: value})
                    else:
                        s = s.filter('wildcard', **{key + keyword: '*' + value + '*'})

        # 处理排序
        sort_list = str2arr(sort)
        if sort_list:
            s = s.sort(*sort_list)  # 排序

        # 分页处理
        page_slice = None
        if (isinstance(page, list) or isinstance(page, tuple)) and len(page) == 2:
            page_slice = slice(page[0], page[1])
            s = s[page_slice]
            func = s.execute
        else:
            func = s.scan

        print('Execute Search Dict:', s.to_dict())

        # 获取结果
        data = {}
        try:
            res = func()
        except Exception as e:
            # 捕捉异常，触发可以处理的异常 `wisdoms 异常`
            # raise
            pass
        else:
            result = [{'id': o.meta.id, **o.to_dict()} for o in res]
            if page_slice:
                data['data'] = result
                data['loc'] = page_slice.start
                data['to'] = page_slice.stop
                data['total'] = res.hits.total.value if hasattr(res.hits.total, 'value') else res.hits.total
            else:
                data = result

        return data


class EsSearch:
    '''
     es查询其实是对repo_ref中get方法的完善（nested查询）
    '''

    def __init__(self, ES_HOST, http_auth=None):
        if isinstance(ES_HOST, list):
            self.es = Elasticsearch(ES_HOST, http_auth=http_auth)
        else:
            self.es = Elasticsearch([ES_HOST], http_auth=http_auth)

    def es_search(self, index, p=None, sort=None, ns_key='id', **kwargs):
        s = Search(using=self.es, index=index)
        for key in kwargs:
            if isinstance(kwargs[key], dict):
                s = s.query('nested', path=key, query=Q('match', **{str(key) + '.' + ns_key: kwargs[key].get(ns_key)}))
            else:
                s = s.filter('term', **{key + '.keyword': kwargs[key]})
        if sort:
            s = s.sort(sort)

        if isinstance(p, list) or isinstance(p, tuple):
            s = s[p[0]:p[1]]
            res = s.execute()
        else:
            res = s.scan()

        return [{"id": o.meta.id, **o.to_dict()} for o in res]

    def paging(self, index: str, searches: dict, page=(0, 50), sort: str = None, types: str = None, **kwargs):
        """
        搜索并带分页功能
        :param index: index名称
        :param searches: 搜索字典
        :param page: (10,20) {"from": 10, "to": 20}
        :param sort: 排序
        :param types: 搜索类型 term, match 默认wildcard模糊搜索
        :param kwargs:
        :return:
        """
        print(kwargs,"what is 参数",searches)
        s = Search(using=self.es, index=index)
        s = s.extra(track_total_hits=True)
        keyword = kwargs.get('keyword') if isinstance(kwargs.get('keyword'), str) else 'keyword'
        if keyword:
            keyword = '.' + keyword
        should_param = []
        detail = kwargs.get('detail', {})
        # 搜索查询
        try:
            # 查询字段在es里面是否存在
            exists_fields_and = detail.get('exists_fields_and_', None)
            exists_fields_or = detail.get('exists_fields_or_', None)
            if isinstance(exists_fields_and, list):
                q = Q()
                for field in exists_fields_and:
                    q = q & Q('exists', field=field)

                s = s.query(q)

            if isinstance(exists_fields_or, list):
                q = None
                for field in exists_fields_or:
                    if q:
                        q = q | Q('exists', field=field)
                    else:
                        q = Q('exists', field=field)

                s = s.query(q)
        except Exception as e:
            print(e)
        # 搜索查询
        if searches:
            for key, value in searches.items():

                types0 = types
                keyword0 = keyword
                reverse0 = False
                exists0 = None
                search0 = "must"
                try:
                    # 获取detail里面字段查询限制
                    extra_limit = detail.get(key)
                    if isinstance(extra_limit, dict):
                        types0 = extra_limit.get('types', types)
                        keyword0 = extra_limit.get('keyword', keyword)
                        reverse0 = extra_limit.get('reverse', False)
                        exists0 = extra_limit.get('exists', None)
                        search0 = extra_limit.get('search',"must")
                        if keyword0:
                            keyword0 = keyword0 if keyword0.startswith('.') else '.' + keyword0
                except Exception as e:
                    print(e)

                # 限制查询字段是否存在
                if exists0 == 'must':
                    s = s.query('exists', field=key)
                if exists0 == 'not':
                    q = ~Q('exists', field=key)
                    s = s.query(q)

                if isinstance(value, dict):
                    # nested 对象查询
                    q = Q()
                    for k, v in value.items():
                        q = q & Q('match', **{str(key) + '.' + k: v})
                    s = s.query('nested', path=key, query=q)
                elif isinstance(value, list):
                    if types0 in ['terms', 'ids']:
                        # 范围查询
                        if search0 == 'should':
                            should_param.append(Q(types0, **{key + keyword0: value}))
                        else:
                            s = s.query(types0, **{key + keyword0: value})
                    elif types0 in ['term', 'match']:
                        # 数组and查询
                        for v in value:
                            if search0 == 'should':
                                should_param.append(Q(types0, **{key + keyword0: v}))
                            else:
                                s = s.query(types0, **{key + keyword0: v})
                    else:
                        if search0 == 'should':
                            should_param.append(Q('range', **{key: {'gte': value[0], 'lte': value[1]}}))
                        else:
                            s = s.query('range', **{key: {'gte': value[0], 'lte': value[1]}})
                elif isinstance(value, int):
                    if types0 in ['term', 'match']:
                        if search0 == 'should':
                            should_param.append(Q(types0, **{key + keyword0: value}))
                        else:
                            s = s.query(types0, **{key + keyword0: value})
                elif value is None:
                    continue
                else:
                    if reverse0:
                        # 取反查询
                        q = ~Q(types0 or 'match', **{key + keyword0: value})
                        s = s.query(q)
                    else:
                        if types0 in ['term', 'match']:
                            if search0 == 'should':
                                should_param.append(Q(types0, **{key + keyword0: value}))
                            else:
                                s = s.filter(types0, **{key + keyword0: value})
                        else:
                            if search0 == 'should':
                                should_param.append(Q('wildcard', **{key + keyword0: '*' + value + '*'}))
                            else:
                                s = s.filter('wildcard', **{key + keyword0: '*' + value + '*'})

        print(should_param, s, "++++++should")
        q = Q('bool',should=should_param)
        s = s.filter(q)
        # 处理排序
        sort_list = str2arr(sort)
        if sort_list:
            s = s.sort(*sort_list)  # 排序

        # 分页处理
        page_slice = None
        if (isinstance(page, list) or isinstance(page, tuple)) and len(page) == 2:
            page_slice = slice(page[0], page[1])
            s = s[page_slice]
            func = s.execute
        else:
            func = s.execute

        print('Execute Search Dict paging+++:',kwargs, s.to_dict())

        # 获取结果
        data = {}
        try:
            res = func()
        except Exception as e:
            # 捕捉异常，触发可以处理的异常 `wisdoms 异常`
            # raise
            pass
        else:
            result = [{'id': o.meta.id, **o.to_dict()} for o in res]
            if page_slice:
                data['data'] = result
                data['loc'] = page_slice.start
                data['to'] = page_slice.stop
                data['total'] = res.hits.total.value if hasattr(res.hits.total, 'value') else res.hits.total
            else:
                data = result

        return data

    def delete_by_ids(self, index: str, ids):
        """
        删除数据，通过ids
        :param index:
        :param ids: id 或者id列表
        :return:
        """
        s = Search(using=self.es, index=index)
        s = s.query('ids', values=ids)
        res = s.delete()
        return res.to_dict()


Repo = BaseRepo
