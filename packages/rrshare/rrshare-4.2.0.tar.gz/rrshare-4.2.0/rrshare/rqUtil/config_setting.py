import json
import os , platform

from rrshare.rqUtil.rqLogs import rq_util_log_info
from rrshare.rqUtil.rqSingleton import Singleton, Singleton_wraps

config_file_dir = ".rrsdk"

# diffrence OS path
path = os.path.expanduser('~')
#rq_util_log_info(path)
rq_path = f'{path}{os.sep}{config_file_dir}' #.format(path, os.sep, '.rrsdk')
#rq_util_log_info(f"{platform.system()}, {path}, {rq_path}")


def get_path_file_name(path_name, file_name):
    # diffrence OS path
    if platform.system() == 'Linux':
        path_name_chg = ''.join([rq_path,'/' ,path_name, '/', file_name])
    if platform.system() == 'Windows':
        path_name_chg =  ''.join([rq_path,'\\', path_name, '\\',file_name])
    #rq_util_log_info(path_name_chg)
    return path_name_chg

path_setting = get_path_file_name('setting','config.json')
rq_util_log_info(path_setting)
path_setting_ini =  get_path_file_name('setting','config.ini')
rq_util_log_info(path_setting_ini)

@Singleton_wraps
class Setting(object):
    def __init__(self, path_config=path_setting):
        self.path_config = path_config
        
    def setting(self):
        config = open(self.path_config)
        return json.load(config)

setting = Setting().setting()
#print(setting)


if __name__ == '__main__':
    #get_path_file_name("setting","config.ini")
    s = Setting()
    #print(id(s), id(Setting()))
    #print(s.setting()['TSPRO_TOKEN'])
    rq_util_log_info(s.setting()['IP_DATABASE_ALIYUN'])

    