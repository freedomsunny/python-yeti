# 认证

认证基于[JWT](https://jwt.io/)

## 添加用户
```python
python3 user_manager.py --username=test --password=test
```
## 获取token
```python
curl --location --request POST 'http://127.0.0.1:8081/v1/token' \
--header 'Content-Type: application/json' \
--data-raw '{"username": "test", "password": "test"}'

{"token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVhdGVkX2F0IjoiMjAyMS0xMi0wNlQwMzo0OToxOCIsImRlbGV0ZWQiOmZhbHNlLCJkZWxldGVkX2F0IjpudWxsLCJpZCI6ImFiYWFkZmJiNTg4MTRjOTk4MWY1NTU2ZTlhNTQ4ODhjIiwicGFzc3dvcmQiOiIkMmIkMTIkeTBoTzMydlpINnVzRmdiY1VwVDUyZVAuaHhRSU1aZFNTdC8yY0RvNVZvSWpGTk5GZmtPU3kiLCJyZWdpc3RyeSI6bnVsbCwic3RhdHVzIjoxLCJ1cGRhdGVkX2F0IjpudWxsLCJ1c2VybmFtZSI6InRlc3QiLCJleHBpcmUiOiIyMDIxLTEyLTA2IDA0OjE5OjI0LjM5MTUwMCJ9.12libt2Qr1iS_c_MndZLk1S-0cHB_r5wp0giOPS0fHc","token_type":"bearer"}
```

## 访问接口
```python
curl 'http://127.0.0.1:8081/helloword' -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVhdGVkX2F0IjoiMjAyMS0xMi0wNlQwMzo0OToxOCIsImRlbGV0ZWQiOmZhbHNlLCJkZWxldGVkX2F0IjpudWxsLCJpZCI6ImFiYWFkZmJiNTg4MTRjOTk4MWY1NTU2ZTlhNTQ4ODhjIiwicGFzc3dvcmQiOiIkMmIkMTIkeTBoTzMydlpINnVzRmdiY1VwVDUyZVAuaHhRSU1aZFNTdC8yY0RvNVZvSWpGTk5GZmtPU3kiLCJyZWdpc3RyeSI6bnVsbCwic3RhdHVzIjoxLCJ1cGRhdGVkX2F0IjpudWxsLCJ1c2VybmFtZSI6InRlc3QiLCJleHBpcmUiOiIyMDIxLTEyLTA2IDA0OjE5OjI0LjM5MTUwMCJ9.12libt2Qr1iS_c_MndZLk1S-0cHB_r5wp0giOPS0fHc'

or

curl 'http://127.0.0.1:8081/helloword?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVhdGVkX2F0IjoiMjAyMS0xMi0wNlQwMzo0OToxOCIsImRlbGV0ZWQiOmZhbHNlLCJkZWxldGVkX2F0IjpudWxsLCJpZCI6ImFiYWFkZmJiNTg4MTRjOTk4MWY1NTU2ZTlhNTQ4ODhjIiwicGFzc3dvcmQiOiIkMmIkMTIkeTBoTzMydlpINnVzRmdiY1VwVDUyZVAuaHhRSU1aZFNTdC8yY0RvNVZvSWpGTk5GZmtPU3kiLCJyZWdpc3RyeSI6bnVsbCwic3RhdHVzIjoxLCJ1cGRhdGVkX2F0IjpudWxsLCJ1c2VybmFtZSI6InRlc3QiLCJleHBpcmUiOiIyMDIxLTEyLTA2IDA0OjE5OjI0LjM5MTUwMCJ9.12libt2Qr1iS_c_MndZLk1S-0cHB_r5wp0giOPS0fHc'

{"result":"hello word"}
```

## 认证相关配置：
```python
# 加密密钥（需修改成你自己的）
secret_key = 6ba4794583c36f6c4e4be05e79dc1ef6df1161cc6737f97670e1696014ebf9b0
# token有效时间，默认30分钟
token_expire_minutes = 30
# 签名算法，默认
algorithm = HS256
# 不进行token验证的API（list类型）
exclude_auth_path = /v1/token,
```


