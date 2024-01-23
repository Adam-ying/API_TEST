import allure
import pytest

from Proj.alivia_Infra.TestData.alivia_infra_query_data import ConstantCompany
from Proj.alivia_Infra.alivia_infra_setting import company_data_json_path
from Proj.alivia_Infra.api_management.common_api import CommonApi
from Util.json_util import OperationJson


@allure.feature("Alivia_Infra 公司case")
class TestCompany:
    def setup_class(self):
        self.db = CommonApi()

    def setup(self):
        self.oj = OperationJson(company_data_json_path)

    @pytest.mark.parametrize("modify_json,expect_value,is_fail_case", [
        ({}, "success", False),
        ({"username": "15170899531"}, None, True),
    ])
    def test_bind_company_by_username(self, hc, modify_json, expect_value, is_fail_case):
        data = self.oj.data['bindCompanyByUserName']
        data['json'].update(modify_json)
        self.db.send_http_request(hc, data=data, query=ConstantCompany.BIND_COMPANY_BY_USERNAME)
        if not is_fail_case:
            # 基础断言
            hc.check_status_code(200)
            # 业务断言
            hc.check_json_path_value("$.data.bindCompanyByUserName.message", expect_value)
        else:
            hc.check_json_path_value_not_equal("$.error[0].message", expect_value)
            pass
        hc.assert_and_show_checkpoint()

    @allure.story('demo1')
    def test_demo1(self):
        assert 1 == 2

    @allure.story('demo2')
    def test_demo2(self):
        assert 1 == 2
