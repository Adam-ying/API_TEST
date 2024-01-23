import os
from Config.base_config import URL_ENV_CONFIG


# 根据项目，环境参数，获取测试url(推荐大家使用， 后续jenkins执行可以选择不同环境进行测试)
def get_url_by_url_env_config(project_line: str, env: str):
    # 获取系统环境变量的值(后期jenkins运行的时候会设置该参数值)
    jenkins_test_env = os.environ.get('API_TEST_URL_ENV')
    if jenkins_test_env:
        # 如果jenkins_test_env环境变量不为空，调用____get_test_url_from_jenkins方法
        return __get_test_url_from_jenkins(project_line, jenkins_env=jenkins_test_env,
                                           origin_env=env)
    else:
        # 如果jenkins_test_env环境变量为空，__get_test_url_base
        return __get_test_url_base(project_line, env)


def __get_test_url_from_jenkins(project_line, jenkins_env, origin_env):
    if project_line not in URL_ENV_CONFIG.keys():
        # 判断如果project_line，不在URL_ENV_CONFIG的key中，使用原始env调用__get_test_url_base
        return __get_test_url_base(project_line, origin_env)
    if jenkins_env not in URL_ENV_CONFIG[project_line].keys():
        # 判断如果jenkins_env， 不在URL_ENV_CONFIG的key中，使用原始env调用__get_test_url_base
        return __get_test_url_base(project_line, origin_env)
    # 如果project_line和jenkins_env都在配置中，则使用jenkins_env变量查找并返回url
    return URL_ENV_CONFIG[project_line][jenkins_env]


def __get_test_url_base(project_line: str, env: str):
    if project_line not in URL_ENV_CONFIG.keys():
        return None
    if env not in URL_ENV_CONFIG[project_line].keys():
        return None
    return URL_ENV_CONFIG[project_line][env]
