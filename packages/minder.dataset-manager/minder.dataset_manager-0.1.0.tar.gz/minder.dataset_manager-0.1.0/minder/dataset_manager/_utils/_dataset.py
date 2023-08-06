import asyncio
import datetime
from os import PathLike
from typing import Any, Dict, List, Union, final
from abc import ABC, abstractmethod
import numpy as np
from minder.research_portal_client.models import ExportJobRequest
from minder.research_portal_client import JobManager


class Dataset(ABC):
    attribute_map: Dict[str, str] = {}

    def __init__(self, *, job_id: List[str]):
        self.__job_id = job_id

    @final
    @property
    def _job_id(self):
        return self.__job_id

    def to_dict(self):
        result = {}

        for attr, attrKey in self.attribute_map.items():
            if hasattr(self, attr):
                value = getattr(self, attr)
                if value is not None:
                    result[attrKey] = value

        result["__job_id"] = self._job_id

        return result

    @final
    def save(self, output_path: Union[str, PathLike]):
        output = self.to_dict()
        np.savez_compressed(output_path, **output)

    @final
    @classmethod
    def load(cls, path: Union[str, PathLike]):
        with np.load(path, mmap_mode="r", allow_pickle=True) as data:
            kwargs = cls._load(data)

        return cls(**kwargs)

    @classmethod
    def _load(cls, data: Dict[str, Any], prefix: str = "") -> Dict[str, Any]:
        kwargs = {}
        for attr, attrKey in cls.attribute_map.items():
            prefixedKey = f"{prefix}{attrKey}"
            if prefixedKey in data:
                kwargs[attr] = data[prefixedKey]

        kwargs["job_id"] = data[f"{prefix}__job_id"].tolist()

        return kwargs

    @classmethod
    def configure(cls, **kwargs) -> None:
        pass

    @classmethod
    @abstractmethod
    def get_latest_data_request(cls, date: datetime.datetime) -> List[ExportJobRequest]:
        pass

    @final
    @classmethod
    async def download(cls, job_ids: List[str], job_manager: JobManager):
        tasks = []
        for job_id in job_ids:
            tasks.append(job_manager.download(job_id))

        result = await asyncio.gather(*tasks)

        files: List[str] = []
        for f in result:
            files.extend(f)

        return files

    @classmethod
    @abstractmethod
    def create(cls, job_id: List[str], files: List[str]):
        pass

    @abstractmethod
    async def update(self, latest_data: "Dataset", *, job_manager: JobManager = None) -> "Dataset":
        self.__job_id.extend(latest_data.__job_id)

        # Remove duplicates
        self.__job_id = list(dict.fromkeys(self.__job_id))

        return self
