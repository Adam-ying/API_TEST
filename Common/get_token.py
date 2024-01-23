from Common.http_client import HttpClient
from Proj.alivia_Infra.TestData.alivia_infra_query_data import ConstantToken
from Proj.alivia_Infra.alivia_infra_setting import token_data_json_path as alivia_Infra_token_data_json_path
from Proj.alivia_Infra.api_management.token_api import TokenAPI
from Util.json_util import OperationJson


class GetTokenStageForAliviaInfra:
    def __init__(self):
        self.hc = HttpClient()
        self.db = TokenAPI()
        self.oj = OperationJson(alivia_Infra_token_data_json_path)

    def get_token(self):
        self.db.send_http_request(self.hc, data=self.oj.data['gettoken_cl'], query=ConstantToken.GET_TOKEN)
        # print(self.hc.res_to_json())
        token = self.hc.json_value("$.data.getToken.token")[0]
        return token

    def get_token2(self):
        self.db.send_http_request(self.hc, data=self.oj.data["gettoken2"], query=ConstantToken.GET_TOKEN)
        token = self.hc.json_value("$.data.getToken.token")[0]
        return token
