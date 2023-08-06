import datetime
import os
import sys
from zenlog import logging
from rrshare.RQSetting.rqLocalize import log_path, setting_path


"""2019-01-03  升级到warning级别 不然大量别的代码的log会批量输出出来
2020-02-19 默认使用本地log 不再和数据库同步
"""

try:
    _name = '{}{}rrshare_{}-{}-.log'.format(
        log_path,
        os.sep,
        os.path.basename(sys.argv[0]).split('.py')[0],
        str(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
    )
except:
    _name = '{}{}rrshare-{}-.log'.format(
        log_path,
        os.sep,
        str(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
    )

logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s RRSHARE>>> %(message)s',
    datefmt='%H:%M:%S',
    filename=_name,
    filemode='w',
)
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
formatter = logging.Formatter('RRSHARE>> %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

logging.info('start RRSHARE')


def rq_util_log_debug(logs, ui_log=None, ui_progress=None):
    logging.debug(logs)


def rq_util_log_info(logs, ui_log=None, ui_progress=None, ui_progress_int_value=None):
    logging.warning(logs)

    # 给GUI使用，更新当前任务到日志和进度
    if ui_log is not None:
        if isinstance(logs, str):
            ui_log.emit(logs)
        if isinstance(logs, list):
            for iStr in logs:
                ui_log.emit(iStr)

    if ui_progress is not None and ui_progress_int_value is not None:
        ui_progress.emit(ui_progress_int_value)


def rq_util_log_expection(logs, ui_log=None, ui_progress=None):
    logging.exception(logs)
    

if __name__ == "__main__":
    rq_util_log_info('test loging info ok!')
    rq_util_log_debug('debug ?')
    
