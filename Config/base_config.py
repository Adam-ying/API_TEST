import os

BaseDTR = os.path.dirname(os.path.dirname(__file__))
extract_yaml_path = os.path.join(BaseDTR, "extract.yaml")


# key值很多地方引用，谨慎修改(公共url配置)
URL_ENV_CONFIG = {
    "whale-alivia": {
        "prod": "https://whale-alivia.meetwhale.com/graphql",
        "stage": "https://whale-alivia.stage.meetwhale.com/graphql"
    },
    "whalewhale": {
        "prod": "https://whalewhale.meetwhale.com/graphql",
        "stage": "https://whalewhale.stage.meetwhale.com/graphql"
    },
    "whaleshop": {
        "stage": "https://whaleshop.stage.meetwhale.com/graphql"
    },
    "tuhu": {
        "stage": "https://tuhu.stage.meetwhale.com/graphql"
    },
    "alivia-tx": {
        "prod": "https://alivia-tx.meetwhale.com/graphql"
    },
    "wop": {
        "stage": "https://stardust.stage.meetwhale.com/graphql",
        "prod": "https://stardust.meetwhale.com/graphql"
    },
    "whale-account-center":{
        "stage": "https://whale-account-center.stage.meetwhale.com/user/login",
    }
}

# 环境路径管理
# 生产环境
# base_url = "https://whale-alivia.develop.meetwhale.com/graphql"

# product环境
# base_url = "https://whaleshop.meetwhale.com/graphql"

# stage环境
base_url = "https://whale-alivia.stage.meetwhale.com/graphql"

# 测试demo环境
# base_url = "https://demo.develop.meetwhale.com/graphql"

# 测试报告聚合平台日志接入接口(线上)
reporter_api_online = "http://10.168.0.10:32498/api/import/execution_data"
reporter_api_online_2 = "http://10.168.0.10:30854/api/import/execution_data"

# 测试报告聚合平台日志接入接口(本地docker)
reporter_api_local = "http://localhost:1180/api/import/execution_data"

webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/cb8d22de-6f35-4858-bb82-593f19055780"


if __name__ == '__main__':
    print(BaseDTR)
    print(os.path.dirname(__file__))