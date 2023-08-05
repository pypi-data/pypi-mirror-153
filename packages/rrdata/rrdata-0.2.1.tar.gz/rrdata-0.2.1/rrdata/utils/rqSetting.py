# coding: utf-8
import configparser
import json
import os
from multiprocessing import Lock
from rrdata.utils.rqLocalize import rq_path, setting_path
from rrdata.utils.config_setting import setting
from rrdata.utils.rqSql import rq_util_sql_postgres_setting

# rrsdk or rrdata有一个配置目录存放在 ~/.rrsdk
# 如果配置目录不存在就创建，主要配置都保存在config.json里面
# 文件的创建步骤，他还会创建一个setting的dir

POSTGRESQL_URI = setting["POSTGRESQL"]
#print(POSTGRESQL_URI)
CONFIGFILE_PATH = '{}{}{}'.format(setting_path, os.sep, 'config.ini')
#print(CONFIGFILE_PATH)

class rq_Setting():

    def __init__(self, uri=None):
        self.lock = Lock()
        self.postgres_uri = uri or self.get_postgres()
        self.username = None
        self.password = None


    def get_postgres(self):
        config = configparser.ConfigParser()
        if os.path.exists(CONFIGFILE_PATH):
            config.read(CONFIGFILE_PATH)
            try:
                res = config.get('POSTGRESQL', 'uri')
            except:
                res =POSTGRESQL_URI
        else:
            config = configparser.ConfigParser()
            config.add_section('POSTGRESQL')
            config.set('POSTGRESQL', 'uri',POSTGRESQL_URI)
            f = open('{}{}{}'.format(setting_path, os.sep, 'config.ini'), 'w')
            config.write(f)
            res =POSTGRESQL_URI
        return res


    def get_config(self,
            section='POSTGRESQL',
            option='uri',
            default_value=POSTGRESQL_URI):
        try:
            config = configparser.ConfigParser()
            config.read(CONFIGFILE_PATH)
            return config.get(section, option)
        except:
            res = self.client.rrquant.usersetting.find_one(
                {'section': section})
            if res:
                return res.get(option, default_value)
            else:
                self.set_config(section, option, default_value)
                return default_value


    def set_config(
            self,
            section='POSTGRESQL',
            option='uri',
            default_value=POSTGRESQL_URI
    ):
        """[summary]
        Keyword Arguments:
            section {str} -- [description] (default: {'POSTGRESQL'})
            option {str} -- [description] (default: {'uri'})
            default_value {[type]} -- [description] (default: {DEFAULT_DB_URI})
        Returns:
            [type] -- [description]
        """
        t = {'section': section, option: default_value}
        self.client.rrquant.usersetting.update(
            {'section': section}, {'$set': t}, upsert=True)

        # if os.path.exists(CONFIGFILE_PATH):
        #     config.read(CONFIGFILE_PATH)
        #     self.lock.release()
        #     return self.get_or_set_section(
        #         config,
        #         section,
        #         option,
        #         default_value,
        #         'set'
        #     )

        #     # 排除某些IP
        #     # self.get_or_set_section(config, 'IPLIST', 'exclude', [{'ip': '1.1.1.1', 'port': 7709}])

        # else:
        #     f = open(CONFIGFILE_PATH, 'w')
        #     config.add_section(section)
        #     config.set(section, option, default_value)

        #     config.write(f)
        #     f.close()
        #     self.lock.release()
        #     return default_value

    def get_or_set_section(
            self,
            config,
            section,
            option,
            DEFAULT_VALUE,
            method='get'
        ):
        try:
            if isinstance(DEFAULT_VALUE, str):
                val = DEFAULT_VALUE
            else:
                val = json.dumps(DEFAULT_VALUE)
            if method == 'get':
                return self.get_config(section, option)
            else:
                self.set_config(section, option, val)
                return val
        except:
            self.set_config(section, option, val)
            return val


    def env_config(self):
        return os.environ.get("POSTGRESURI", None)

    @property
    def client(self):
        return rq_util_sql_postgres_setting(self.postgres_uri)


#rqSETTING = rq_Setting()
#DATABASE = rqSETTING.client

