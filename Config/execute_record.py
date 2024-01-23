
# 项目执行信息（只需填写基础信息）
PROJECT_EXECUTE_INFO = {
    "Marketing_Center": {
        'projectKey': '9f99326573f94736a3007cd64f0ccf9b',  # 项目key <获取方式：从测试报告聚合平台中获取>
        'executor': 'API自动化',
        'type': 1,  # 测试类型 <1-API，2-WebUI、3-Android、4-iOS>
        'tag': 3,   # 分类标签 <1-冒烟测试，2-全量回归, 3-单接口, 4-多接口场景>
    },
    # "account_center": {
    #     'projectKey': '53ce8763d4984a248ac66e48064955a9',
    #     'executor': 'API自动化',
    #     'type': 1,
    #     'tag': 3,
    # },
    "alivia_Infra": {
        'projectKey': '5ba70758c73e413a82f2105b7da56bf4',
        'executor': 'API自动化',
        'type': 1,
        'tag': 3,
    },
    "oms": {
        'projectKey': 'c945cbbf7bb34a49a6c2e583349aec80',
        'executor': 'API自动化',
        'type': 1,
        'tag': 3,
    },
    "analytics": {
        'projectKey': '9775e3b9f91241f4b288b3925c3f1fcc',
        'executor': 'API自动化',
        'type': 1,
        'tag': 3,
    },
    "Digital_Intelligence_web": {
        'projectKey': 'ee592b59b1fd4ae3b48fc5a24810f9d8',
        'executor': 'API自动化',
        'type': 1,
        'tag': 3,
    },
    "Content_Intelligence_Dam": {
        'projectKey': '17b39ea53a3a418eb8357ee775cd49c8',
        'executor': 'API自动化',
        'type': 1,
        'tag': 3,
    },
    "Zdemo": {
        'projectKey': '1e8df10533234923924976af20a64115',
        'executor': '本地调试',
        'type': 1,
        'tag': 3,
    },
    "Zdemo2": {
        'projectKey': 'xxxxxxxxxxxxxxxxxx',
        'executor': '本地调试',
        'type': 1,
        'tag': 3,
    },
}




"""
    项目执行记录完整配置如下
    {
        "projectKey": "项目key <获取方式：从测试报告页面中生成>",
        "executor": "执行者",
        "type": "测试类型 <1-API测试，2-WebUI测试、3-MobileUI测试>",
        "tag": "分类标签 <1-冒烟测试，2-全量回归>",
        "startTime": "开始时间 <时间戳>",
        "endTime": "结束时间 <时间戳>",
        "caseList": [
            {
                "caseId": "用例ID <可以使用uuid>",
                "caseName": "用例名称",
                "caseDesc": "用例描述",
                "FeatureDesc": "关联的Feature描述",
                "duration": "执行时间(毫秒)",
                "status": "用例状态<1-未执行,2-执行中,3-测试通过,4-测试失败,5-异常终止>",
                "logs": [
                    {
                        "type": "前置条件",
                        "detail": ""
                    },
                     {
                        "type": "接口请求信息",
                        "detail": ""
                    },
                    {
                        "type": "接口响应信息",
                        "detail": ""
                    },
                    {
                        "type": "接口验证信息",
                        "detail": ""
                    },
                    。。。。。。。。。。。。。
                ]
            },
        ],
    }
"""

