# 获取项目路径
import datetime
import os.path

# 获取项目路径
import uuid


def project_path():
    return os.path.dirname(os.path.dirname(__file__))


# 递归创建目录
def mkdir(path):
    path = path.strip()  # 去除首位空格
    path = path.rstrip("//")
    is_exists = os.path.exists(path)

    # 判断结果
    if not is_exists:
        os.makedirs(path)
        return True
    else:
        return False


def get_uuid():
    return "".join(str(uuid.uuid4()).split("-"))


def time_diff_stamp(start_stamp, end_stamp):
    """
     求两个时间戳差值：时 分 秒 毫秒
    :param start_stamp: 开始时间戳
    :param end_stamp:  结束时间戳
    :return:
    """
    start_dt = datetime.datetime.fromtimestamp(start_stamp)
    end_dt = datetime.datetime.fromtimestamp(end_stamp)
    result = end_dt - start_dt
    hours = int(result.seconds / 3600)
    minutes = int(result.seconds % 3600 / 60)
    seconds = int(result.seconds % 3600 % 60)
    ms = round(result.microseconds / 1000)
    return "{0}时{1}分{2}秒{3}毫秒".format(hours, minutes, seconds, ms)


if __name__ == '__main__':
    get_uuid()
