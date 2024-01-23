from Proj.Zdemo2.TestData.test_data import host, login_acc, login_pwd
from Common.http_client import BodyType
from Common.http_client import HttpClient
from Proj.Zdemo2.TestData.api_data import Login_Token


class CommonAPI:
    """ 公共接口请求类 """

    def __init__(self, headers_flag=True):
        self.headers_flag = headers_flag
        if self.headers_flag:
            self.headers = {'Access-Token': GetToken().get_token()}

    def send_http_request(self, hc, api_data):
        hc.set_name(name=api_data["case_name"])     # 配置接口名称
        hc.set_method(method=api_data["method"])    # 配置请求方法
        hc.set_url(url=host+api_data["url"])        # 配置请求地址
        if self.headers_flag:
            hc.set_headers(headers=self.headers)     # 配置请求头
        if api_data.get("body_type", None):
            hc.set_body_type(body_type=api_data['body_type'])  # 配置请求正文体类型
        if api_data.get("body", None):
            hc.set_body(data=api_data['body'])    # 配置请求正文体
        if api_data.get("params", None):
            hc.set_params(params=api_data['params'])  # 配置请求参数
        hc.send()  # 发送请求


class GetToken:
    """ 获取登录token类 """

    def __init__(self):
        self.hc = HttpClient()
        self.ca = CommonAPI(headers_flag=False)

    def get_token(self):
        api_data = {
            "case_name": "登录接口",
            "method": Login_Token.GET_TOKEN[0],
            "url": Login_Token.GET_TOKEN[1],
            "body_type":  Login_Token.GET_TOKEN[2],
            "body": {"username": login_acc, "password": login_pwd},
            "params": None
        }
        self.ca.send_http_request(self.hc, api_data=api_data)
        token = self.hc.json_value("$..data.token")[0]
        return token