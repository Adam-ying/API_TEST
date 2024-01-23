import os
import time
from functools import wraps

import pytest

from Common.http_client import HttpClient
from Common.log_report import LogReport
from Util.logger_util import info_log
from Util.yamls_util import clear_extract_yaml


def retry(try_limit=3, interval_time=1, log_show=True):
    """
    失败重跑
    :param try_limit:
    :param interval_time:
    :param log_show:
    :return:
    """

    def try_func(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try_cnt = 0
            while try_cnt < try_limit:
                st = time.time()
                scenarios_result = func(*args, **kwargs)
                info_log(f"\n\nscenarios_result --------- {scenarios_result}\n\n")
                et = time.time()
                if log_show:
                    info_log("%s: DONE %s" % (func.__name__, (et - st)))
                if "成功" not in scenarios_result:
                    try_cnt += 1
                    time.sleep(interval_time)
                    if log_show:
                        info_log("%s: RETRY CNT %s" % (func.__name__, try_cnt))
                else:
                    break

        return wrapper

    return try_func


@pytest.fixture(scope="session", autouse=True)
def clear_extract():
    """
    备注：由于配置了在一次session中清理yaml关联参数的步骤，所以单独跑单接口关联用例会有问题，批量执行正常
    """
    clear_extract_yaml()


@pytest.fixture(scope="session", autouse=True)
def proj_config(request):
    """
    记录 整个项目执行起止时间（项目维度执行一次）
    :param request: 钩子函数-执行请求
    :return:
    """
    os.environ["LOG_NAME"] = request.config.getoption("--log-name")  # 日志名称（项目名称）
    os.environ["REPORT_ENV"] = request.config.getoption("--report-env")  # 日志上报的环境（聚合报告平台、venus平台）
    os.environ["EXECUTOR"] = request.config.getoption("--executor")  # 执行者
    os.environ["API_TYPE"] = request.config.getoption("--api-type")  # 接口类型
    os.environ["EXECUTE_ENV"] = request.config.getoption("--execute-env")  # 执行的环境
    os.environ["CASE_MARK"] = request.config.getoption("--case-mark")  # 用例标记
    # os.environ["TEST_TYPE"] = request.config.getoption("--test-type")  # 测试类型
    # os.environ["PROJECT_KEY"] = request.config.getoption("--project-key")  # 测试类型

    info_log(f"项目开始时间：{time.time()}\n\n")
    yield
    info_log(f"项目结束时间：{time.time()}")
    time.sleep(1)
    if os.environ.get("REPORT_ENV") != "venus":
        print("将日志结果上报聚合报告平台")
        LogReport().run()


@pytest.fixture(scope="function", autouse=True, name="hc")
# @retry(try_limit=3, interval_time=1)
def case_config():
    """ 记录 每个用例执行执行起止时间（每一个用例都会执行）"""
    info_log(f"用例开始时间：{time.time()}\n")
    # 备注：本地调试 由于无法传参 API_TYPE 所以默认为single
    if os.environ.get('API_TYPE', "") == "single":
        http_client = HttpClient()
        yield http_client
        # 判断是否为本地执行（本地执行多接口场景用例时， hc.name为空）
        if http_client.name:
            http_client.get_case_result()  # 获取用例执行结果并显示日志
            # http_client.notice_with_fail() # 若存在失败用例则发送飞书通知
            http_client.notice_with_fail_format()  # 格式化之后发送
        else:
            pass
    else:
        yield
    info_log(f"用例结束时间：{time.time()}\n\n")

# 配置命令行获取参数
def pytest_addoption(parser):
    """ 注册自定义参数到配置对象 """
    # 控制：上报日志的项目名称
    parser.addoption("--log-name", action="store", default="", help="上报日志的项目名称（默认不上报）")
    # 控制： 区分上报日志的环境、失败用例是否发送飞书通知（venus：不上报日志，将执行结果回调推送给venus平台）
    parser.addoption("--report-env", action="store", default="offLine", choices=["offLine", "onLine", "venus"], help="日志上报环境")
    # 控制：测试执行者
    parser.addoption("--executor", action="store", default="API自动化", help="执行者")
    # 控制：接口测试类型（ tag ）分类标签 <1-冒烟测试，2-全量回归, 3-单接口, 4-多接口场景>
    parser.addoption("--api-type", action="store", default="single", choices=["single", "scenarios"], help="接口类型")
    # 控制：区分执行环境
    parser.addoption("--execute-env", action="store", default="stage", choices=["test", "stage", "prod"], help="执行环境")
    # 控制：执行用例标记
    parser.addoption("--case-mark", action="store", default="None", help="用例标记")
    # # 控制：测试类型标记 ( type ) <1-API，2-WebUI、3-Android、4-iOS>
    # parser.addoption("--test-type", action="store", default="stage", choices=["API", "WebUI", "Android", "iOS"], help="测试类型")
    # # 控制：项目KEY
    # parser.addoption("--project-key", action="store", help="项目KEY")

def pytest_collection_modifyitems(items):
    """
     测试用例收集完成时，将收集到的item的name和nodeId的中文显示在控制台上
     （解决 用例名称 ids=[] 显示乱码的问题）
    :param items:
    :return:
    """
    for item in items:
        item.name = item.name.encode('utf-8').decode('unicode-escape')
        item._nodeid = item.nodeid.encode('utf-8').decode('unicode-escape')
