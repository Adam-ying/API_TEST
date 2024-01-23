import os.path

from Common.get_proj_url import get_url_by_url_env_config

# stage环境url
from Config.base_config import BaseDTR

stage_url = "https://whale-alivia.stage.meetwhale.com/graphql"
base_url = get_url_by_url_env_config("whale-alivia", "stage")

# test_data 目录
json_data_base_dir = os.path.join(BaseDTR, "Proj/alivia_Infra/TestData/")

# 测试数据json文件路径
token_data_json_path = os.path.join(BaseDTR, json_data_base_dir, "token_data.json")
company_data_json_path = os.path.join(BaseDTR, json_data_base_dir, "company_data.json")



if __name__ == "__main__":
    
    print(base_url)