import pytest
from Proj.Zdemo2.TestData.api_data import Module_Name
from Proj.Zdemo2.CommonConfig.common_api import CommonAPI
from Common.http_client import HttpClient
from Common.scenarios_check import ScenariosCheck


class TestScenariosName:

    def setup_class(self):
        self.ca = CommonAPI()  # 初始化公共接口对象（获取登录token）

    def setup(self):
        self.sc = ScenariosCheck()  # 初始化 场景用例检查对象

    def teardown(self):
        self.sc.get_scenario_case_result()  # 获取 场景用例执行结果
        self.sc.notice_with_fail()  # 若存在失败用例则发送飞书通知

    @pytest.mark.parametrize("scenarios_name, type, startTime, endTime, exp_code, exp_lineName",
                             [('场景测试用例_01', "1", "2022-08-22 00:00:00", "2022-08-22 23:59:59", 1000, "内容智能产品线")])
    def test_scenarios_01(self, scenarios_name, type, startTime, endTime, exp_code, exp_lineName):
        """
            接口1：新增接口（ 验证新增成功，并获取新增记录的id ）
            接口2：查询接口（ 通过新增的id进行查询，验证新增的数据能够查询到 ）
            接口3：删除接口（ 通过新增的id进行删除，验证删除成功 ）
            接口4：查询接口（ 通过新增的id进行查询，验证无法查询到相应的数据）

            场景配置步骤：
            1.配置场景用例名称
            2.每个接口的配置步骤（ 整体放入'try-exception'中捕获异常情况并作异常标记 ）
             （1）配置接口参数
             （2）初始化'接口检查对象'并发送请求
             （3）添加基础检查点
             （4）添加业务检查点
             （5）'场景用例检查对象'添加'接口检查对象'
            3.场景断言并显示检查点结果
        """
        # 配置场景用例名称
        self.sc.add_scenarios_name(scenarios_name=scenarios_name)
        try:
            # -------------------------------- 接口1 新增接口 --------------------------------
            # 配置接口参数
            api_data = {
                "case_name": "获取测试记录列表",
                "method": Module_Name.getPlanList[0],
                "url": Module_Name.getPlanList[1],
                "body_type": Module_Name.getPlanList[2],
                "body": {"type": type, "startTime": startTime, "endTime": endTime},
                "params": None
            }
            # 初始化'接口检查对象'并发送请求
            hc = HttpClient()
            self.ca.send_http_request(hc=hc, api_data=api_data)
            # 添加基础检查点
            hc.check_status_code(exp=200, msg="检查http响应码")
            hc.check_response_less_than(exp=2000, msg="检查响应时间")
            # 添加业务检查点
            act_code = hc.json_value(path="$.code")[0]  # 从接口响应中获取实际的code值
            hc.check_assert_equal(arg1=exp_code, arg2=act_code, msg="接口响应码正确")
            # '场景用例检查对象'添加'接口检查对象'
            self.sc.add_api_hc(hc=hc)

            # 获取新增的 第一条测试记录ID
            planId_list = hc.json_value("$.data..planId")
            first_planId = planId_list[0]
            print(f"first_planId -------- {first_planId}")

            # -------------------------------- 接口2 查询接口 --------------------------------
            # 配置接口参数
            api_data = {
                "case_name": "获取第一条测试记录报告",
                "method": Module_Name.getPlanReport[0],
                "url": Module_Name.getPlanReport[1].replace("<planId>", first_planId),
                "body_type": Module_Name.getPlanReport[2],
                "body": None,
                "params": None
            }

            # 初始化'接口检查对象'并发送请求
            hc = HttpClient()
            self.ca.send_http_request(hc=hc, api_data=api_data)
            # 添加基础检查点
            hc.check_status_code(exp=200, msg="检查http响应码")
            hc.check_response_less_than(exp=2000, msg="检查响应时间")
            # 添加业务检查点
            act_lineName = hc.json_value(path="$.data..lineName")[0]  # 从接口响应中获取实际的code值
            hc.check_assert_equal(arg1=exp_lineName, arg2=act_lineName, msg="检查产品线名称")

            # '场景用例检查对象'添加'接口检查对象'
            self.sc.add_api_hc(hc=hc)

        except Exception as e:
            self.sc.add_error_flag()

        # 场景断言并显示检查点结果
        self.sc.assert_and_show_checkpoint()