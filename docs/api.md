# 接口开发说明
## 定义接口：
所有业务接口文件必须以.py结尾，必须包含在yeti/api/handlers目录中。API需要加载的目录可通过配置项: api_load_dirs进行配置。__init__.py不会被加载
```python
from fastapi import APIRouter
router = APIRouter(tags=["example"],
                   )


@router.get("/")
async def say_hello():

    return {"Hello": "World====="}

```
**关键点**：
1. 必须引入APIRouter并实例化。实例化中的tags参数可自行定义，访问docs时会按显标签进行分类
2. @router.get("/") 代表定义了一个路径为/，方法为GET的接口。
3. 接口定义完成后，框架将自动加载。无需其他任何操作。

## query参数
[query参数定义](https://fastapi.tiangolo.com/tutorial/query-params/)

## Path参数
[Path参数定义](https://fastapi.tiangolo.com/tutorial/path-params/)
## 请求body检查
定义数据结构 比如：为创建用户的接口/v1/users定义数据结构
1. 创建存放数据结构的文件（可选）
2. 定义数据结构、
```python
from pydantic import BaseModel
from typing import Optional


class UsersScheme(BaseModel):
    username: str
    age: int
    address: Optional[str] = ""


class ExampleScheme(BaseModel):
    user: UsersScheme
    foo: str
    bar: str
```
3. 接口引用
```python
@router.post("/test")
def post_example(item: ExampleScheme):

    return {"it": item}

其中ExampleScheme类等价于如下JSON数据：
{
  "user": {
    "username": "string",
    "age": 0,
    "address": ""
  },
  "foo": "string",
  "bar": "string"
}
```
更多示例请参考：[请求body定义](https://fastapi.tiangolo.com/tutorial/body/)

4. 定义接口返回数据，用于自动生成Swagger文档。将以下代码定义在yeti/api/common/data_scheme/目录下
```python

from typing import Any, Optional, List
from pydantic import BaseModel, Field

from yeti.api.common.dependencies import CommonResponseModel


class ProductPricingResponse(CommonResponseModel):
    class PricingData(BaseModel):
        class ProductPricingAssociate(BaseModel):
            attr_id: str = "atr_G7gE5GX7MQY7"
            uint: str = "分钟"

        class ProductPricingStrategies(BaseModel):
            class Filters(BaseModel):
                filter_id: str = "flt_R8523kVXoy6q"
                left_value: str = "patr_PackageMonth"
                right_value: str = "12"
                operator: str = "=="

            strategy_id: str = "stg_0PPx8RV3Wy6q"
            basic_discount: int = Field(default=1000, title="折扣")
            cost_expression: str = Field(default="1000", title="价格")
            filter_expression: str = "flt_v5nD1DEvozXN&&flt_R8523kVXoy6q"
            filters: List[Filters]
            name: str = "strname_nr8BEo8WGkOB"
            remark: str = ""

        prod_id: str = "prd_Pk5q0lOA1vzJ"
        plan_id: str = "plan_RXAZX5ov3ME3"
        comp_id: str = "comp_kWooO9xVyl8g"
        name: str = "test3333"
        billing_mode: str = "package_resource"
        pricing_mode: str = "enum"
        update_time: str = "2021-10-08T08:10:35Z"
        associate: ProductPricingAssociate
        strategies: List[ProductPricingStrategies]
        comp_code: str = "comp_kWooO9xVyl8g"
        mapping_comp_id: str = Field(default="", title="映射id")
        mapping_name: str = Field(default="", title="映射名称")

    data: PricingData
```
以上代码等价于如下json:
```python
{
  "business_code": 200,
  "msg_en": "success",
  "msg_cn": "成功",
  "data": {
    "prod_id": "prd_Pk5q0lOA1vzJ",
    "plan_id": "plan_RXAZX5ov3ME3",
    "comp_id": "comp_kWooO9xVyl8g",
    "name": "test3333",
    "billing_mode": "package_resource",
    "pricing_mode": "enum",
    "update_time": "2021-10-08T08:10:35Z",
    "associate": {
      "attr_id": "atr_G7gE5GX7MQY7",
      "uint": "分钟"
    },
    "strategies": [
      {
        "strategy_id": "stg_0PPx8RV3Wy6q",
        "basic_discount": 1000,
        "cost_expression": "1000",
        "filter_expression": "flt_v5nD1DEvozXN&&flt_R8523kVXoy6q",
        "filters": [
          {
            "filter_id": "flt_R8523kVXoy6q",
            "left_value": "patr_PackageMonth",
            "right_value": "12",
            "operator": "=="
          }
        ],
        "name": "strname_nr8BEo8WGkOB",
        "remark": ""
      }
    ],
    "comp_code": "comp_kWooO9xVyl8g",
    "mapping_comp_id": "",
    "mapping_name": ""
  },
  "count": 0
}
```
接口使用response：
```python
from fastapi import status
from yeti.api.common.data_scheme import ProductPricingResponse, CommonResponseModel

@router.post("/test", response_model=ProductPricingResponse,  response_model_exclude_unset=True)
def post_example(item: ExampleScheme):
    data = {}
    return CommonResponseModel(data=resource_pkgs,
                               business_code=status.HTTP_200_OK,
                               msg_cn="成功",
                               msg_en="Success",
                               count=0
                               )
```
**关键点**
1. 定义完响应类后，需要在接口路由处引用。@router.post("/test", **response_model=ProductPricingResponse**)；
2. 支持多层嵌套，适合复杂数据结构；
3. 接口return时，需要用CommonResponseModel进行响应，包如下参数：
    business_code       业务代码
    msg_en              英文消息
    msg_cn              中文消息
    data                数据
    count               数据总条数
4.  response_model_exclude_unset=True 参数用于控制当返回数据为空时，定义的空model不会被返回

## 请求body高级用法
### 1. 定义多个返回models
```python
from pydantic import BaseModel

class Example_200_Mask(BaseModel):
    code: str = 200

class Example_422_Mask(BaseModel):
    code: str = 402
    details: str = "Error happened"

class Example_Mask(BaseModel):

    class Config:
        schema_extra = {
                "200": {"model": Example_200_Mask},
                "422": {"model": Example_422_Mask},
        }

# 接口处引用
@app.post("/mask", responses=Example_Mask.Config.schema_extra)
```
### 2. 定义多个请求models
```python
from fastapi import FastAPI
from typing import Union
from pydantic import BaseModel

class User(BaseModel):
    name: str

class Item(BaseModel):
    size: int
    price: float

app = FastAPI()

@app.post("/multi/")
def process_things(body: Union[User, Item]):
    return body

```

## 中间件(装饰器)
在请求到达时，需要做一些处理时可以用到此功能。比如，记录请求日志

```python
async def request_logging(request: Request):
    """
    请求日志记录
    :param request:
    :return:
    """
    try:
        json_body = await request.json()
    # may be not json
    except (UnicodeDecodeError, JSONDecodeError):
        json_body = b""
    request_context = dict(
        client_ip=str(request.client),
        requests_url=str(request.url),
        request_headers=dict(Headers(request.headers)),
        request_method=request.method,
        request_body=json_body
    )
    LOG.info("Incoming request: {}".format(HttpLoggingRequestContext(**request_context).dict())
             )

# 定义完涵数后，将方法加入到该列表中
# 顺序: 列表越靠前越优先执行
before_request_middlewares = [
    request_logging
]
```

## 请求上下文
针对每个请求，需要保存一些全局变量的。可按如下方法实现。如：保存用户的认证信息
```python
from yeti.api.common.g import g

async def user_auth(request: Request):
    try:
        json_body = await request.json()
    # may be not json
    except (UnicodeDecodeError, JSONDecodeError):
        json_body = b""
    user_info = headers_authorize(headers=dict(Headers(request.headers)),
                                  method=request.method,
                                  req_data=json_body,
                                  query_args=request.query_params,
                                  req_path=request.url.path
                                  )
    # 保存
    g().user_info = user_info

# 读取
userinfo = g().user_info
```

## Websocket
本框架的websocket解决了多进程、多节点间通信问题。使用方法：
```python
from typing import Any
from fastapi import WebSocket, WebSocketDisconnect
from fastapi import APIRouter

from yeti.api import get_app
from yeti.api.handlers.ws import ws_connector
from yeti.exceptions import exceptions
from yeti.cfg import CONF

app = get_app()
router = APIRouter(tags=["websocket"],
                   )


# if CONF.enable_websocket is True:
@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: Any):
    # Accept new client connect
    await ws_connector.connect(websocket)
    try:
        while True:
            message = await websocket.receive_text()
            if message:
                # 广播消息，每个节点&进程都会收到
                await ws_connector.send_message(message=message)
    except WebSocketDisconnect:
        # 用户离开消息，每个节点&进程都会收到
        await ws_connector.disconnect(websocket, "{} has disconnect".format(client_id)
                                      )
```

## CORS跨域
CORS已在中间件层处理，允许所有跨域请求。
````python
yeti/api/common/middlewares.py

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

````


## 文件上传
文件上传接口也定义在handlers目录中。通过form表单上传，示例代码如下：
```python
from fastapi import APIRouter
from fastapi import File, UploadFile

from yeti.cfg import CONF

router = APIRouter(tags=["files"]
                   )


@router.post("/upload/")
async def create_upload_file(file: UploadFile = File(...)):
    # 文件名
    file_name = file.filename
    # 类型
    content_type = file.content_type
    # 实际数据
    data = await file.read()
    # 文件大小(byte)
    file_size = len(data)
    # 写数据
    f = open("test.txt", "a+")
    f.write(data)
    f.close()
    return {"filename": file.filename}
```

## 认证
[认证](auth.md#认证)

## 接口文档
启动项目后，API文档自动生成(Swagger), 访问: http://yourhost:yourport/docs 查看
