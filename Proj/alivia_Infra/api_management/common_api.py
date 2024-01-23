from Common.get_token import GetTokenStageForAliviaInfra
from Common.http_client import BodyType
from Config.base_config import base_url


class CommonApi:
    def __init__(self):
        self.post_method = "POST"
        self.headers = {'authorization': GetTokenStageForAliviaInfra().get_token()}

    def send_http_request(self, hc, data, query):
        hc.set_name(name=data["case_name"])
        hc.set_url(url=base_url)
        hc.set_method(method=self.post_method)
        hc.set_headers(headers=self.headers)
        hc.set_body_type(body_type=BodyType.JSON)
        hc.set_body(data={'query': query, 'variables': data['json']})
        hc.send()
