from Common.http_client import BodyType


# 登录接口
class Login_Token:
    # ( 请求方式、请求地址、正文体类型 )
    GET_TOKEN = ("POST", "/api/user/login", BodyType.JSON)


# 模块名(类名) - 接口名(类属性)
class Module_Name:
    getProTestRes = ("GET", "/api/dashboard/product_test_res", None)
    getPlanList = ("POST", "/api/plan/list", BodyType.JSON)
    getPlanReport = ("GET", "/api/plan/report/<planId>", None)
