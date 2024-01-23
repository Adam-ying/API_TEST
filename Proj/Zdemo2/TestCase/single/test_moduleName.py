import allure
import pytest
from Proj.Zdemo2.TestData.api_data import Module_Name
from Proj.Zdemo2.CommonConfig.common_api import CommonAPI


class TestModuleName:

    def setup_class(self):
        self.ca = CommonAPI()  # 初始化公共接口对象（获取登录token）

    @pytest.mark.QUERY_API
    @pytest.mark.parametrize("case_name, projectName, exp_code",
                             [('获取某产品的测试执行结果_01', "android_xueqiu_app", 1000),
                              ('获取某产品的测试执行结果_02', "android_xueqiu_app", 1001)])
    def test_single_01(self, hc, case_name, projectName, exp_code):
        """
            单接口配置步骤：1.配置接口参数、2.发送请求、3.添加基础检查点、4.添加业务检查点、5.单接口断言并显示检查点结果
        """
        # 1.配置接口参数
        api_data = {
            "case_name": case_name,
            "method": Module_Name.getProTestRes[0],
            "url": Module_Name.getProTestRes[1],
            "body_type": Module_Name.getProTestRes[2],
            "body": None,
            "params": {"projectName": projectName}
        }
        # 2.发送请求（ hc=检查点对象, api_data=接口请求参数 ）
        self.ca.send_http_request(hc=hc, api_data=api_data)

        # 3.添加基础检查点
        hc.check_status_code(exp=200, msg="检查http响应码")  # 检查http响应码是否为200
        hc.check_response_less_than(exp=2000, msg="检查响应时间")  # 检查响应时间是否小于等于2秒

        # 4.添加业务检查点
        act_code = hc.json_value(path="$.code")[0]  # 从接口响应中获取实际的code值
        hc.check_assert_equal(arg1=exp_code, arg2=act_code, msg="接口响应码正确")

        # 5.单接口断言并显示检查点结果
        hc.assert_and_show_checkpoint()

    @allure.story('demo1')
    def test_demo1(self):
        assert 1 == 1

    @allure.story('demo2')
    def test_demo2(self):
        assert 1 == 2