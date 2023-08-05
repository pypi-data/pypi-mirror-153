import json
# from dapr.clients import DaprClient
import requests


def dapr_invoke(*, host="localhost", app, method, data, http_verb="post", **kwargs):
    """
    dapr http invoke

    :param app: app_id
    :param method: 方法名称
    :http_verb: http请求方法
    :return:
    """
    if (http_verb == "get"):
        return requests.get(
            f"http://{host}:3500/v1.0/invoke/{app}/method{method}", params=data)
    elif (http_verb == "post"):
        return requests.post(
            f"http://{host}:3500/v1.0/invoke/{app}/method{method}", json=data)
    # with DaprClient() as d:
    #     res = d.invoke_method(
    #         app, method, json.dumps(data), http_verb=http_verb, **kwargs
    #     )
    #     return res


def dapr_pubsub(data, pubsub_name="pubsub", topic_name="topic", **kwargs):
    """
    dapr pubsub

    :param pubsub_name: pubsub名称
    :param topic_name: topic名称
    :param data: 数据
    :return:
    """
    with DaprClient() as d:
        res = d.publish_event(
            pubsub_name=pubsub_name,
            topic_name=topic_name,
            data=json.dumps(data),
            data_content_type="application/json",
        )
