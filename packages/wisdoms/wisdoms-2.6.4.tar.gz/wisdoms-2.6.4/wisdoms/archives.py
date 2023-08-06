# Created by Q-ays.
# whosqays@gmail.com

from wisdoms.ms import rpc_wrapper

"""
archive = archive_config('announce', 'announcement', {'name': '公告服务', 'service': 'announcementService'}, MS_HOST)

@rpc
@user_
def announce_add(self, origin):
    data = origin.get('data')

    data['create_time'] = datetime.now()
    data['addTime_'] = datetime.now()

    announce = ar.add(data)

    archive(origin, '添加公告', o2d(announce))

    return success2d(announce)

传入origin自动获取用户信息，组织信息，请求数据

"""


def archive_config(archive_index, form_index, service, host):
    """
    存档配置生成
    :param archive_index:存档index
    :param form_index: 表单index
    :param service: 项目微服务信息配置
    :param host: rabbit mq 配置
    :return:
    """
    origin = dict()
    origin['index'] = archive_index
    data = dict()
    data['service'] = service
    data['index'] = form_index
    origin['data'] = data

    def archive_save(info_: dict = None, desc_: str = None, resp_data_=None, event_=True, struct_=False, **kwargs):
        """
        :param info_: 原始信息结构，带有用户信息
        :param desc_: 操作描述
        :param resp_data_: 返回数据
        :param event_: 发送事件的方式存储
        :param struct_: 返回存储数据结构
        :param kwargs: 存档数据结构，可自动添加额外信息
        :return:
        """
        if isinstance(info_, dict):
            data['user'] = info_.get('user')
            data['org'] = info_.get('org')
            data['req_data'] = info_.get('data')
            if isinstance(data['req_data'], dict):
                data['order_id'] = data['req_data'].get('order_')
        data['desc'] = desc_
        data['resp_data'] = resp_data_
        data.update(kwargs)

        if struct_:
            return {'data': origin}

        if event_:
            try:
                res = rpc_wrapper('archivesFunc', 'dispatch', {'data': origin}, host_=host, timeout_=2)
                return res
            except Exception as e:
                print(e)
                print('archive service error')
                return 'archive service error'
        else:
            try:
                res = rpc_wrapper('archivesFunc', 'add', {'data': origin}, host_=host, timeout_=8)
                return res
            except Exception as e:
                print(e)
                print('archive service error')
                return 'archive service error'

    return archive_save
