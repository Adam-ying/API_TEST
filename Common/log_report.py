import json
import os

import requests

from Config.base_config import reporter_api_online, reporter_api_online_2, reporter_api_local
from Config.execute_record import PROJECT_EXECUTE_INFO
from Util.tools import project_path, mkdir, get_uuid, time_diff_stamp


class LogReport(object):
    """ 执行日志上报 聚合报告平台"""

    def __init__(self, log_name=None, api_type=None, report_env=None):
        self.project_execute_info = None  # 项目执行信息（基础）
        self.log_file = None  # 日志文件
        self.executor = os.environ.get("EXECUTOR", "API自动化")  # 执行者
        self.execute_env = os.environ.get("EXECUTE_ENV", "stage")  # 执行环境
        self.report_env = report_env and report_env or os.environ.get("REPORT_ENV",
                                                                      "offLine")  # 上报日志的环境 onLine | offLine
        self.log_name = log_name and log_name or os.environ.get("LOG_NAME", "")  # 上报日志的项目名称
        self.api_type = api_type and api_type or os.environ.get("API_TYPE", "single")  # 接口类型（单接口、多接口）

    def run(self):
        """ 解析并上报日志平台 """
        if self.log_name:
            self.get_config_info()
            if self.log_file is not None and self.project_execute_info is not None:
                self.record_execute_info()  # 从日志中 记录执行信息
                self.integration_case_data()  # 整合用例数据
                # self.execute_info_import_db()  # 执行信息导入数据库（调用API）

    def get_config_info(self):
        """ 获取日志名称对应的配置信息 """
        # 获取对应的日志文件
        log_dir = os.path.join(project_path(), 'Logs')  # 日志记录
        mkdir(log_dir)
        log_name_list = os.listdir(log_dir)  # 日志文件列表
        log_file_name = f"{self.log_name}.log"
        if log_file_name in log_name_list:
            self.log_file = os.path.join(log_dir, log_file_name)
        # 获取对应的项目执行信息（基础）
        for projectName, execute_info in PROJECT_EXECUTE_INFO.items():
            if projectName == self.log_name:
                # 根据pytest命令行参数 替换 执行信息（基础）数据
                execute_info["executor"] = self.executor
                execute_info["tag"] = self.api_type == "scenarios" and 4 or 3
                execute_info["env"] = self.execute_env
                execute_info["caseMark"] = os.environ.get("CASE_MARK", "None")

                # print("----------------------------------")
                # print(execute_info)
                # print("----------------------------------")

                self.project_execute_info = {projectName: execute_info}

    def record_execute_info(self):
        """
            【 从日志中 记录执行信息 】
            格式如下：
            project_execute_info = {
                "Marketing_Center": {
                    'projectKey': '9b6881ccc7fa403bb283e61b52c0204b'
                    'executor': '费晓春',
                    'type': 1,
                    'tag': 2,
                    'startTime': 1649334733.037964,
                    'endTime': 1649334751.49514,
                    'caseData': [
                        {
                            '用例开始时间': 1649334733.037964
                            '场景名称[scenarios_name]': xxxxx // ( 针对多接口场景用例 )
                            '用例名称[name]': login
                            '请求地址[url]': https://whaleshop.meetwhale.com/graphql
                            '请求方式[method]': post
                            '请求头文件[headers]': {'content-type': 'application/json'}  // 若存在则记录
                            '请求参数[params]': {'uname':'xxx', 'pwd':'xxx'}  // 若存在则记录
                            '正文体类型[body_type]': JSON   // 若存在则记录
                            '请求正文体[body]': {'key':'value',}  // 若存在则记录
                            '响应状态码': 200
                            '响应时间(ms)': 789
                            '响应体[body]': {"errno":10000,"errmsg":"success","data":{}}
                            '检查点[1]': xxxx
                            '检查点[2]': xxxx
                            '测试结果': 接口验证成功
                            '用例结束时间'：1649334751.49514
                        },
                    ]
                },
            }
        """
        for projectName, execute_info in self.project_execute_info.items():
            # 获取日志中的所有行 lines
            with open(self.log_file, encoding="utf-8") as file_obj:
                lines = file_obj.readlines()
            caseData = []  # 记录所有用例列表
            case_dict = dict()  # 记录日志中同一个用例的相关数据
            flag = 3  # 作为匹配某用例相关数据的标记 （1_当前为用例起始标记、2_当前为用例中间标记、3_当前为用例结束标记）
            for line in lines:
                if line == "\n":
                    continue
                # 记录项目基础信息：项目开始时间戳、项目结束时间戳
                if "项目开始时间" in line:
                    startTime = line.split("项目开始时间：")[1].strip()
                    execute_info["startTime"] = float(startTime)
                if "项目结束时间" in line:
                    endTime = line.split("项目结束时间：")[1].strip()
                    execute_info["endTime"] = float(endTime)
                if "=== None" in line:  # 处理特殊情况
                    flag = 3
                    case_dict = dict()
                    continue
                # 记录用例基础信息
                if flag == 3:
                    if "用例开始时间" in line:
                        flag = 1
                        # print(line)
                        # print(line.split("'用例开始时间': ")[1].strip())
                        case_dict["用例开始时间"] = line.split("用例开始时间：")[1].strip()
                elif flag == 1:
                    flag = 2

                    type_key, detail_value = self.parse_type_detail(line)
                    print(type_key, detail_value)
                    if type_key:
                        case_dict[type_key] = detail_value
                elif flag == 2:
                    if "用例结束时间" in line:
                        flag = 3
                        case_dict["用例结束时间"] = line.split("用例结束时间：")[1].strip()
                        caseData = self.del_repeat_case(caseData, case_dict)
                        case_dict = dict()
                    else:
                        # print(f"line ------ {line}")
                        type_key, detail_value = self.parse_type_detail(line)
                        if type_key:
                            case_dict[type_key] = detail_value
            execute_info['caseData'] = caseData
            # print(execute_info)

    def parse_type_detail(self, line):
        """ 解析单条日志记录，获取 type detail """
        type_key, detail_value = "", ""
        if " - INFO - " in line:
            tmp_list = line.split(" - INFO - ")
        elif " - ERROR - " in line:
            tmp_list = line.split(" - ERROR - ")
        else:
            tmp_list = line.split(" - WARNING - ")
        if len(tmp_list) == 2:
            content = tmp_list[1]
            if "===" in content:
                td = content.split("===")
                if len(td) == 2:
                    type_key = td[0].strip()
                    detail_value = td[1].strip()
        return type_key, detail_value

    def del_repeat_case(self, caseData, case_dict):
        """
        剔除'失败重跑'中重复执行的用例
        :param caseData: 当前已保存的用例字典列表
        :param case_dict: 当前准备保存的用例字典

        [ 判断重复的条件 ]
            用例名称[name]、请求地址[url]、请求方式[method]、正文体类型[body_type]、请求正文体[body] 是否全部一致
            （ 备注：请求头文件[headers] 中会存在不同的token 所以不能作为去重条件 ）

            [ 处理逻辑 ]
            比较：'当前已保存的用例字典列表'中的最后一个 与 '当前准备保存的用例字典'
            1.若重复
            （1）先 去掉最后一个用例
            （2）再 添加新用例
            2.若不重复
            （1）直接添加新用例
        """
        add_flag = True  # 添加用例的标记
        if caseData:
            case_last = caseData[-1]
            if self.api_type == "single":
                no_case_name = case_dict.get("用例名称[name]", "没有用例名称Key")
                if no_case_name == "没有用例名称Key":
                    # print(f"\n case_dict --- {case_dict} \n")
                    add_flag = False
                elif case_last["用例名称[name]"] == case_dict["用例名称[name]"] \
                        and case_last["请求地址[url]"] == case_dict["请求地址[url]"] \
                        and case_last["请求方式[method]"] == case_dict["请求方式[method]"] \
                        and case_last["正文体类型[body_type]"] == case_dict["正文体类型[body_type]"] \
                        and case_last["请求正文体[body]"] == case_dict["请求正文体[body]"]:
                    caseData.pop()
            else:  # 多接口场景
                last_screnarios_name = case_last.get("场景名称[scenarios]")
                current_screnarios_name = case_dict.get("场景名称[scenarios]")
                if last_screnarios_name == current_screnarios_name:
                    caseData.pop()

        if add_flag:
            caseData.append(case_dict)
        return caseData

    def integration_case_data(self):
        """
            整合用例数据  ( 将 caseData 数据格式 装换成 caseList 数据格式 )
            A.若不存在 caseData 数据 则直接剔除 该项目
            B.若存在 caseData 数据
                1.整合用例基础信息数据
                （1）生成 caseId： uuid
                （2）计算 'duration': 用例执行时间
                （3）转换 'status'：用例状态 <1-未执行,2-执行中,3-测试通过,4-测试失败,5-异常终止>
                2.整合用例详情
                （1）将其余键值对 存入 logs 字典列表中 { 'type': '', 'detail': ''}
                格式如下：
                project_execute_info = {
                    "Marketing_Center": {
                        'projectKey': '9b6881ccc7fa403bb283e61b52c0204b'
                        'executor': '费晓春',
                        'type': 1,
                        'tag': 2,
                        'startTime': 1649334733.037964,
                        'endTime': 1649334751.49514,
                        'caseList': [
                            {
                                'caseId': uuid()
                                'caseName': xxxx
                                'caseDesc':  xxxx
                                'FeatureDesc': xxxx
                                'duration': 计算用例执行时间
                                'status'："用例状态<1-未执行,2-执行中,3-测试通过,4-测试失败,5-异常终止>"
                                'logs'：[ { 'type': xxxx, 'detail': xxxx }, ]
                            },
                        ]
                    },
                }
        """
        no_log_projectName_list = []
        for projectName, execute_info in self.project_execute_info.items():
            caseData = execute_info.get('caseData', '')
            if caseData:
                # 将 caseData 数据格式 装换成 caseList 数据格式
                caseList = []
                for each in caseData:
                    # print(each)
                    case = dict()
                    case['caseId'] = get_uuid()
                    # print(f'{each["用例结束时间"]}---------------------{each["用例结束时间"]}')
                    if self.api_type == "single":
                        case["caseName"] = each.get("用例名称[name]")
                    else:  # 多接口场景
                        case['caseName'] = each.get("场景名称[scenarios]")
                    case['caseDesc'] = ""
                    case['FeatureDesc'] = ""
                    case['duration'] = time_diff_stamp(float(each["用例开始时间"]), float(each["用例结束时间"]))
                    if each.get("测试结果") in ["接口验证成功", "接口场景验证成功"]:
                        case['status'] = 3
                    elif each.get("测试结果") in ["接口验证失败", "接口场景验证失败"]:
                        case['status'] = 4
                    elif each.get("测试结果") in ["接口验证异常", "接口场景验证异常"]:
                        case['status'] = 5
                    else:
                        case['status'] = 5
                    logs = []
                    for key, value in each.items():
                        # print(key, value)
                        if key not in ['用例开始时间', '用例结束时间']:
                            logs.append({'type': key, 'detail': value})
                    case['logs'] = logs
                    caseList.append(case)
                execute_info['caseList'] = caseList
                del execute_info['caseData']
            else:
                no_log_projectName_list.append(projectName)
        # 则直接剔除 没有日志的项目PROJECT_EXECUTE_INFO
        for projectName in no_log_projectName_list:
            del self.project_execute_info[projectName]

    def execute_info_import_db(self):
        """ 执行信息导入数据库（调用API）"""
        pro_dict = list(self.project_execute_info.values())[0]
        headers = {"Content-Type": "application/json"}
        if self.report_env == "onLine":
            try:
                resp = requests.post(url=reporter_api_online, headers=headers, json=pro_dict)
            except Exception as e:
                resp = requests.post(url=reporter_api_online_2, headers=headers, json=pro_dict)
        else:
            resp = requests.post(url=reporter_api_local, headers=headers, json=pro_dict)
        resp.encoding = "utf-8"
        resp_dict = json.loads(resp.text)
        print(resp_dict)

        # # 调试打印
        # pro_dict = list(self.project_execute_info.values())[0]
        # for key, value in pro_dict.items():
        #     if key == "caseList":
        #         print(f"打印 caseList 数量 --------- {len(value)}")
        #         for k, v in value[0].items():  # 只显示第一条用例结果
        #             if k == "logs":
        #                 for each in v:
        #                     for a, b in each.items():
        #                         print(f"        {a} === {b}")
        #             else:
        #                 print(f"    {k} === {v}")
        #     else:
        #         print(f"{key} === {value}")

    def show(self):
        print('\n日志文件')
        print(f'log_file --- {self.log_file}')
        print('\n项目执行信息')
        if self.project_execute_info:
            for projectName, execute_info in self.project_execute_info.items():
                print(f"projectName --- {projectName}")
                for key, value in execute_info.items():
                    print(f'{key}: {value}')
                    if key == "caseList":
                        print(len(value))
                        for case in value:
                            for k, v in case.items():
                                print(f"{k} ---- {v}")
                            print(f"{'-' * 300}\n")

        else:
            print(f"project_execute_info ---- {self.project_execute_info}")


if __name__ == '__main__':
    lr = LogReport(log_name="Zdemo2", api_type="scenarios")  # single scenarios
    lr.log_name = 'Zdemo2'
    lr.run()
    lr.show()
