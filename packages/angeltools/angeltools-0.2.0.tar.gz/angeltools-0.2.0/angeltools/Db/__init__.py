import os


def get_uri_info(uri_name, default_uri, uri_only=False):
    """
    从环境变量中提取并拆解 mongo redis mysql 连接器的 uri 为独立参数
    :param uri_name:    uri的环境变量名
    :param default_uri: 如果没有，则使用默认uri
    :param uri_only:    只返回uri，不拆解
    :return:            uri, user, passwd, host, port, db
    """
    if os.environ.get(uri_name):
        uri = os.environ.get(uri_name)
    else:
        uri = default_uri
    if uri_only:
        return uri
    param_temp = uri.split("//")[-1]
    if '/' in param_temp:
        param, db = param_temp.split("/")
    else:
        param = param_temp.split("/")[0]
        db = ''
    if '@' in param:
        host_port = param.split('@')[-1]
        user_password = '@'.join(param.split('@')[:-1])
    else:
        user_password = ':'
        host_port = param
    user = user_password.split(":")[0]
    passwd = ":".join(user_password.split(":")[1:])
    host, port = host_port.split(":")
    return uri, user, passwd, host, port, db
