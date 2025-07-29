import logging

from pydantic import BaseModel, SecretStr

from ..api import DBCaseConfig, DBConfig, MetricType

log = logging.getLogger(__name__)


class AliyunOpenSearchConfig(DBConfig, BaseModel):
    host: str = ""
    user: str = ""
    password: SecretStr = ""
    index_type:str ="DiskANN"
    def to_dict(self) -> dict:
        return {
            "host": self.host,
            "user": self.user,
            "password": self.password.get_secret_value(),
            "index_type": self.index_type
        }


class AliyunOpenSearchIndexConfig(BaseModel, DBCaseConfig):
    metric_type: MetricType = MetricType.L2
#    ef_construction: int = 500

#    M: int = 100
#    ef_search: int = 40
    
    pq_dims: int = 8
    max_degree: int = 64
    build_list_size: int = 100
    thread_count: int = 16
    search_list_size: int = 300
    io_limit: int = 300
    beam: int = 8
    def distance_type(self) -> str:
        if self.metric_type == MetricType.L2:
            return "SquaredEuclidean"
        if self.metric_type in (MetricType.IP, MetricType.COSINE):
            return "InnerProduct"
        return "SquaredEuclidean"

    def index_param(self) -> dict:
        return {}

    def search_param(self) -> dict:
        return {}
