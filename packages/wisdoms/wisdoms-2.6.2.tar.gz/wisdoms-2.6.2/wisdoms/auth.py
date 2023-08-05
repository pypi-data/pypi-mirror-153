from wisdoms.exec import UserException


class InnerAuth:

    @staticmethod
    def all_true(*args):
        """
        所有为真通过
        :param args:
        :return:
        """
        for a in args:
            if a:
                pass
            else:
                raise UserException('权限验证失败')

    @staticmethod
    def one_true(*args):
        """
        验证至少一个为真则通过
        :param args:
        :return:
        """
        for a in args:
            if a:
                return

        raise UserException('权限验证失败')

    @staticmethod
    def mget(origin, key, exc='用户权限获取异常'):
        value = origin.get(key)

        if value is not None:
            return value
        else:
            raise UserException(exc)

    def permit_get(self, origin):
        return self.mget(origin, 'permit', '代理权限异常-agent exception')

    def privilege_get(self, origin):
        permit = self.permit_get(origin)
        return self.mget(permit, 'privilege', '获取用户特殊权限失败-privilege exception')

    def level_get(self, origin):
        privilege = self.privilege_get(origin)
        return self.mget(privilege, 'level', '获取用户特殊权限等级失败-privilege level exception')

    def role_get(self, origin):
        privilege = self.privilege_get(origin)
        return self.mget(privilege, 'role', '获取用户特殊权限角色失败-privilege role exception')

    def role_judge(self, origin, role0):
        role = self.role_get(origin)

        return role == role0

    def bloc(self, origin):
        """
        判断当前是否是集团代理用户
        :param origin:
        :return: boolean
        """
        return self.role_judge(origin, 'bloc')

    def agent(self, origin):
        """
        判断当前是否是区域代理用户
        :param origin:
        :return: boolean
        """
        return self.role_judge(origin, 'agent')

    def admin(self, origin):
        """
        判断是否是平台管理员用户
        :param origin:
        :return: boolean
        """
        return self.role_judge(origin, 'admin')

    def super(self, origin):
        """
        判断是否是超级管理用户
        :param origin:
        :return: boolean
        """
        return self.role_judge(origin, 'super')

    def region_in(self, origin, region0):
        """
        检查区域id是否在代理范围内
        :param origin:
        :param region0:
        :return: boolean
        """
        permit = self.permit_get(origin)
        region = self.mget(permit, 'region', '代理区域获取异常-region get exception')

        return region0 in region and self.agent(origin)

    def agent_in(self, origin, agent0):
        """
        检查子代理是否在代理范围内
        :param origin:
        :param agent0:
        :return: boolean
        """
        permit = self.permit_get(origin)
        agent = self.mget(permit, 'agent', '子代理用户获取异常-sub agent get exception')

        return agent0 in agent and self.agent(origin)

    def org_in(self, origin, org0):
        """
        检查组织id是否在代理组织列表内
        :param origin:
        :param org0:
        :return: boolean
        """
        permit = self.permit_get(origin)
        org = self.mget(permit, 'org', '代理组织获取异常-org get exception')

        return org0 in org and self.agent(origin)


auth = InnerAuth()
