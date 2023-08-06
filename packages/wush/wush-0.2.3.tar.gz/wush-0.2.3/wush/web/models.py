
from datetime import datetime
from typing import ( Dict, Any)
from csarg.parser import Argument
from pydantic import ( BaseModel, Field, validator)
from wush.common.run_mode import RunMode

from .enums import MethodEnum, RequestsParamsEnum
from .curl_utils import cUrl

__all__ = ['RequestBuilder']

def create_version() -> str:
    return datetime.now().strftime('%Y%m%d%H%M%S_%s')

class RequestBuilder(BaseModel):
    """请求构造器"""
    version: str = Field(title="版本号", default_factory = create_version)
    url: str = Field(..., title="地址")
    method: str = Field(MethodEnum.GET.value, title="请求方式")
    params: Dict[str, Any] = Field({}, title="地址参数")
    json_data: Dict[str, Any] = Field({}, title="json 参数", alias="json")
    body: str = Field(None, title="body 参数")
    headers: Dict[str, Any] = Field({}, title="headers 参数")
    cookies: Dict[str, Any] = Field({}, title="cookies 参数")
    run_mode: RunMode = Field(None, title="运行模式")
    argument: Argument = Field(None, title="参数解析器")

    class Config:
        arbitrary_types_allowed = True

    @validator('method')
    def check_and_format_method(cls, v: str) -> str:
        v = v.upper()
        MethodEnum.validate(v)
        return v

    @classmethod
    def load_curl(cls, curl_file):
        """加载 curl 的本文文件"""
        params = cUrl.dump(curl_file)
        ins = cls(**params)
        ins.format()
        return

    def add_headers(self, **kwargs):
        """添加 headers"""
        self.headers.update(kwargs)

    def add_cookies(self, **kwargs):
        """添加 cookies"""
        self.cookies.update(kwargs)

    def set_run_mode(self, mode):
        self.run_mode = RunMode(mode)

    def to_requests(self):
        """转换为 requests 参数"""
        data = {}
        for key in RequestsParamsEnum.values():
            try:
                data[key] = getattr(self, key)
            except:
                pass
        data['json'] = self.json_data
        return data


class Header(BaseModel):
    content_type: str = Field(None, alias='Content-Type')
    content_length: int = Field(None, alias='Content-Length')
    server: str = Field(None, alias='Server')
    date: str = Field(None, alias='Date')
    connection: str = Field(None, alias='Connection')
    accept_ranges: str = Field(None, alias='Accept-Ranges')
    etag: str = Field(None, alias='ETag')
    cache_control: str = Field(None, alias='Cache-Control')
    expires: str = Field(None, alias='Expires')
    last_modified: str = Field(None, alias='Last-Modified')
    location: str = Field(None, alias='Location')

    class Meta:
        origin_data: Dict[str, str] = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.Meta.origin_data = kwargs

    def __getitem__(self, key: str) -> str:
        return self.Meta.origin_data[key]

    def get(self, key: str) -> str:
        return self.Meta.origin_data.get(key)

    def __setattr__(self, key: str, value: str) -> AttributeError:
        raise AttributeError('\'Header\' object does not support attribute assignment')




