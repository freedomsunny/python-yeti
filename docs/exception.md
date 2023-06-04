# 异常
## 定义异常
自定义异常需要在yeti/exceptions/exceptions.py中
```python
class ParameterError(ErrorBase):
    """参数错误"""
    msg_cn = "参数 %(parm)s 不合法"
    msg_en = "parameter %(parm)s invalid"
    http_code = status.HTTP_400_BAD_REQUEST
    business_code = constants.PARAMETER_ERROR_CODE

直接继承ErrorBase
msg_cn              中文消息
msg_en              英文消息
http_code           http状态码
business_code       业务代码，在yeti/exceptions/constants.py中定义
```

## 使用异常
```python
raise ParameterError(parm="user_name", http_code=400)
```

## 异常接口返回
在代码中raise的异常接口将以JSON返回给调用方，如下，自定义了异常类AuthError
```python
class AuthError(ErrorBase):
    """认证失败"""
    msg_cn = "认证失败"
    msg_en = "user %(user_id)s auth fail"
    http_code = status.HTTP_401_UNAUTHORIZED
    business_code = constants.AUTHENTICATION_ERROR_CODE
```
引发异常：
```python
raise exceptions.AuthError(msg_en="Missing 'Date' in headers",
                           msg_cn="缺少http头'Data'"
                           )
```
接口返回：
```python
{"business_code":100001,"msg_en":"Missing 'Date' in headers","msg_cn":"缺少http头'Data'","data":{},"count":0}
```
