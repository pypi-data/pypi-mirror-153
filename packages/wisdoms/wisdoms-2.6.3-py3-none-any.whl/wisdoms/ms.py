# Used for micro-service which developed by dapr
# install dapr before use
from fastapi import Header, HTTPException
from wisdoms.dapr import dapr_invoke


def add_uid(host="localhost",app_id="base_app", method="/base/get_uid"):
    """
    验证用户token并且返回用户id
    :return: dict
    """

    def uid_(token=Header(alias="x-token", default=None)):
        if token == None or token == "":
            raise HTTPException(status_code=200, detail="未填写token信息")
        userInfo = dapr_invoke(host=host,app=app_id, method=method, data={"token": token}).json()
        if userInfo["code"] == 1:
            return userInfo["data"]
        else:
            raise HTTPException(status_code=200, detail=userInfo["desc"])

    return uid_


def add_user(host="localhost",app_id="base_app", method="/base/get_user"):
    """
    验证用户token并返回用户信息
    :extra: app_id 基础应用微服务名称
    :extra: method 获取用户信息方法名称
    :return: dict
    """

    def user_(token=Header(alias="x-token", default=None)):
        if token == None or token == "":
            raise HTTPException(status_code=200, detail="未填写token信息")
        res = dapr_invoke(host=host,app=app_id, method=method, data={"token": token}).json()
        if res["code"] == 1:
            userInfo = res["data"]
            # TODO 查看原来的代码，添加哪些字段
            org = None
            try:
                # 添加组织信息 add info of org
                org = userInfo.get("org").get(str(userInfo.get("current_org")))
            except:
                pass
            try:
                # delete user passoword
                del userInfo["password"]
                del userInfo["partner"]
            except:
                pass
            cut_user = dict()
            cut_org = dict()
            cut_user["id"] = userInfo["id"]
            cut_user["account"] = userInfo["account"]
            cut_user["username"] = userInfo.get("username")
            cut_user["current_org"] = userInfo.get("current_org")
            cut_user["phone"] = userInfo.get("phone")
            cut_user["recommend_phone"] = userInfo.get("recommend_phone")
            cut_user["agent_oid"] = userInfo.get("agent_oid")
            cut_user["from_agent"] = userInfo.get("from_agent")
            cut_user["member_phone"] = userInfo.get("member_phone")
            cut_user["email"] = userInfo.get("email")
            cut_user["avatar"] = userInfo.get("avatar")
            cut_user["appid"] = userInfo.get("appid")
            cut_user["openid"] = userInfo.get("openid")
            cut_user['roles'] = [r.role for r in userInfo.get("roles")]
            # TODO????
            try:
                if org:
                    cut_org["id"] = org["id"]
                    cut_org["name"] = org["name"]
                    cut_org["desc"] = org.get("desc")
                    cut_org["owner"] = org.get("owner")
                    cut_org["region"] = org.get("region")
                    cut_org["es_extend"] = org.get("es_extend")
                    cut_org["share_profit_id"] = org.get("share_profit_id")
                    cut_org["mch_id"] = org.get("mch_id")
                    cut_org["sp_appid"] = org.get("sp_appid")
                    cut_org["appid"] = org.get("appid")
                    cut_org["images"] = org.get("images")
                    cut_org["videos"] = org.get("videos")
                    cut_org["location"] = org.get("location")
            except:
                pass
            response = {"uid": userInfo.get("id"), "user": cut_user, "org": cut_org}
            return response
        else:
            raise HTTPException(status_code=200, detail=res["desc"])

    return user_
