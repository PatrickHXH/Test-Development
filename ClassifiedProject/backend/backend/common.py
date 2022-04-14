class Error:
    '''
    定义错误码与错误信息
    '''
    USER_OR_PAWD_NULL = {"10010":"用户名或密码为空"}
    USER_OR_PAWD_EROOR={"10011":"用户名或密码错误"}
    PAWD_ERROR = {"10012":"两次密码不一致"}
    USER_EXIST = {"10013":"用户已被注册"}
    PROJECT_NAME_EXIST={"10014":"项目名字已存在"}
    PROJECT_NOT_EXIST={"10015":"项目不存在"}
    PROJECT_IS_DELETE = {"10016":"项目已删除"}
    FLIE_TYPE_ERROR = {"10017":"不支持该文件类型上传"}

    MODULE_NAME_EXIST={"10018":"模块名字已存在"}
    MODULE_NOT_EXIST={"10019":"模块不存在"}
    MODULE_IS_DELETE = {"10020":"模块已删除"}

    CASE_METHOD_ERROR = {"10051":"请求方法错误"}
    CASE_HEADER_ERROR = {"10052":"请求header错误"}
    CASE_PARAMS_ERROR = {"10053":"请求参数类型错误"}
    CASE_ASSERT_ERROR = {"10054":"请求参数类型错误"}
    CASE_DELETE_ERROR = {"10055":"用例已删除"}

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