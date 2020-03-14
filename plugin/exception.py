class ApiError(Exception):
    '''
        {
            code: 400,
            msg: ''
        }
    '''

    def __init__(self, value, code=400):
        self.value = value
        self.code = code

    def __str__(self):
        return repr(self.value)


class ServerError(ValueError):
    '''
        {
            code: 500,
            msg: ''
        }
    '''
    pass


class ForbiddenError(ValueError):
    '''
        {
            code: 403,
            msg: '无权限'
        }
    '''
    pass


class UnauthorizedError(ValueError):
    '''
        {
            code: 401,
            msg: '未登录'
        }
    '''
    pass


class NotFoundError(ValueError):
    '''
        {
            code: 404,
            msg: '接口不存在'
        }
    '''
    pass