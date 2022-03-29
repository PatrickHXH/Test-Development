class Error:
    '''
    定义错误码与错误信息
    '''
    USER_OR_PAWD_NULL = {"10010":"用户名或密码为空"}
    USER_OR_PAWD_EROOR={"10011":"用户名或密码错误"}
    PAWD_ERROR = {"10012":"两次密码不一致"}
    USER_EXIST = {"10013":"用户已被注册"}


def response(success:bool = True, error = None, result=[]):
    if error is None:
        error_code = ""
        error_msg = ""
    else:
        success = False
        error_code = list(error.keys())[0]
        error_msg = list(error.values())[0]
    '''
    定义统一返回格式
    '''
    resp_dict = {
        "success":success,
        "error":{
            "code":error_code,
            "msg":error_msg
        },
        "result" : result
    }
    return resp_dict