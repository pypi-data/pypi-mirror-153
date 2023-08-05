# Created by Q-ays.
# whosqays@gmail.com

# install PYyaml before use

"""
    Example::

        from wisdoms.config import c
        c.get('name')
"""

import yaml
from wisdoms.utils import joint4path


def read_env(f):
    return f.read().strip()


def read_config(f):
    try:
        return yaml.full_load(f)
    except Exception as e:
        print(e)
        return yaml.load(f)


def find_file(func, path, desc=' '):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            result = func(f)
            if result:
                print('~~~~~~~~~~~~~~~~~~~~~~ success ~~~~~~~~~~~~~~~~~~~~~')
                print(desc, 'file path is', path, '\n')
                return result
            else:
                print('~~~~~~~~~~~~~ warning ~~~~~~~~~~~~~~~~~~')
                print('contents of ', path, ' is None' '\n')
                return {}
                # raise Exception('contents of ' + str(desc) + ' file is None')
    except FileNotFoundError:
        print(desc, 'file path', path, ' match failed \n')
        return False


class Config:
    """
    读取yml配置文件
    """

    def __init__(self, layer=4):
        """
        可自动定义层数
        :param layer:
        """
        self.configuration = dict()

        # find .env file and read
        env_path = '.env'
        ms_path = 'global.yml'
        env = None
        for i in range(layer):
            env = find_file(read_env, env_path, '.env')

            if env:
                try:
                    self.configuration.update(find_file(read_config, ms_path, 'common config'))
                except Exception as e:
                    print('load global config failed, viz. global.yml')
                    print(e)
                break
            else:
                env_path = joint4path('..', env_path)
                ms_path = joint4path('..', ms_path)

        # find config.yml file and read
        if env:
            config_path = joint4path('config', str(env) + '.yml')

            for i in range(layer):
                configuration = find_file(read_config, config_path, 'config')

                if isinstance(configuration, dict):
                    self.configuration.update(configuration)
                    break
                else:
                    config_path = joint4path('..', config_path)
        else:
            print('~~~~~~~~ can not find .env file :< ~~~~~~~~~~')

    def get(self, key):
        if isinstance(self.configuration, dict) and self.configuration:
            return self.configuration.get(key)
        else:
            return {'err_code': 'maybe environment variable is missed'}

    def to_dict(self):
        if self.configuration:
            return self.configuration


c = Config(5)
