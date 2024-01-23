from Config.base_config import extract_yaml_path


def clear_extract_yaml():
    with open(extract_yaml_path, "w", encoding="utf-8") as f:
        f.truncate()

