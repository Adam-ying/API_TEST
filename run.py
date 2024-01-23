import os

import pytest

import sys

from Config.execute_record import PROJECT_EXECUTE_INFO
from Config.testcase_path_config import PROJECT_TESTCASE_PATH_INFO


def get_running_args():
    args = sys.argv[1:]
    args_dict = {}
    for arg in args:
        if "=" not in arg:
            continue
        key, value = arg.split("=")
        args_dict[key] = value
    if "API_TEST_URL_ENV" in args_dict:
        # 设置临时环境变量，是在代码运行时生效
        os.environ["API_TEST_URL_ENV"] = args_dict.get("API_TEST_URL_ENV")
    return args_dict


def _run_project(project, jenkins_dir):
    # 如果项目未配置用例路径，跳过。执行下一个项目
    if project not in PROJECT_TESTCASE_PATH_INFO.keys():
        print("运行{}项目测试用例-未配置用例路径".format(project))
        return

    # 获取对应项目的用例路径配置
    proj_testcase_path_dict = PROJECT_TESTCASE_PATH_INFO.get(project, {})
    print("项目用例路径配置", proj_testcase_path_dict)

    # 执行项目的指定路径用例
    single_path = proj_testcase_path_dict.get("single_path", None)
    print("single_path", single_path)
    scenarios_path = proj_testcase_path_dict.get("scenarios_path", None)
    print("scenarios_path", scenarios_path)

    # 单接口用例运行
    if single_path is not None and single_path != "":
        pytest_main_run_args = []
        # pytest_main_run_args.append("-q")
        pytest_main_run_args.append(jenkins_dir + "Proj/" + project + single_path)
        # pytest_main_run_args.append("--html="+jenkins_dir+"reports/report.html")
        pytest_main_run_args.append("--log-file=" + jenkins_dir + "Logs/" + project + ".log")
        pytest_main_run_args.append("--log-name=" + project)
        pytest_main_run_args.append("--report-env=onLine")
        pytest.main(pytest_main_run_args)
    else:
        print(f"{project}没有配置单接口用例路径:{single_path}")
    # 场景接口用例运行
    if scenarios_path is not None and scenarios_path != "":
        pytest_main_run_args = []
        # pytest_main_run_args.append("-q")
        pytest_main_run_args.append(jenkins_dir + "Proj/" + project + scenarios_path)
        pytest_main_run_args.append("--html=" + jenkins_dir + "reports/report.html")
        pytest_main_run_args.append("--log-file=" + jenkins_dir + "Logs/" + project + ".log")
        pytest_main_run_args.append("--log-name=" + project)
        pytest_main_run_args.append("--report-env=onLine")
        pytest_main_run_args.append("--api-type=scenarios")
        pytest.main(pytest_main_run_args)
    else:
        print(f"{project}没有配置场景接口用例路径:{scenarios_path}")


def run_proj_jenkins():
    print("Run Testcase on jenkins")
    # 本地调试
    # AUTO_API_TEST_JENKINS_DIR = ""
    # jenkins 项目目录
    AUTO_API_TEST_JENKINS_DIR = "API_TEST/"
    args_dict = get_running_args()
    print("运行参数字典", args_dict)
    print("获取环境'API_TEST_URL_ENV'变量的值", os.environ.get("API_TEST_URL_ENV"))
    proj_name = args_dict.get("Project_Name")
    print(proj_name)
    if proj_name is None:
        print("未指定运行目录")
        return
    if proj_name == "ALL":
        for run_proj in PROJECT_EXECUTE_INFO.keys():
            print("运行{}项目测试用例".format(run_proj))
            _run_project(project=run_proj, jenkins_dir=AUTO_API_TEST_JENKINS_DIR)
    else:
        if proj_name not in PROJECT_EXECUTE_INFO.keys():
            print("该项目未配置到聚合报告平台运行列表中。。")
            return
        print("运行{}项目测试用例".format(proj_name))
        _run_project(project=proj_name, jenkins_dir=AUTO_API_TEST_JENKINS_DIR)


if __name__ == '__main__':
    # jenkins 运行
    run_proj_jenkins()
    # python ./run.py Project_Name=Marketing_Center
