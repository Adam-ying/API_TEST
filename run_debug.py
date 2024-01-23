import pytest


def debug(run_proj, api_type, executor, report_env='onLine', execute_env="stage", mark=None):
    """
        execute_env : 执行环境 stage | prod （ 仅供日志报告展示使用，实际切环境需要手动去'TestData'文件中进行切换）
    """
    pytest_main_run_args = []
    if mark:
        pytest_main_run_args.append("-m" + mark)
        pytest_main_run_args.append("--case-mark" + mark)
    pytest_main_run_args.append("./Proj/" + run_proj + "/TestCase/" + api_type)
    pytest_main_run_args.append("--log-file=./Logs/" + run_proj + ".log")
    pytest_main_run_args.append("--log-name=" + run_proj)
    pytest_main_run_args.append("--executor=" + executor)
    pytest_main_run_args.append("--api-type=" + api_type)
    pytest_main_run_args.append("--report-env=" + report_env)
    pytest_main_run_args.append("--execute-env=" + execute_env)
    pytest.main(pytest_main_run_args)

if __name__ == '__main__':
    debug(run_proj="alivia_infra", api_type="single", executor="执行者")