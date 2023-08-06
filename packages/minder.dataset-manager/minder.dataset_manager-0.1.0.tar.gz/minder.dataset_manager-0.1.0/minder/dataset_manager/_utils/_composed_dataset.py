import asyncio
import datetime
from typing import Any, Dict, List, Tuple, Type, Union, cast, final
from minder.research_portal_client.models import ExportJobRequest
from minder.research_portal_client import JobManager
from minder.dataset_manager._utils import Dataset


class ComposedDataset(Dataset):
    _dataset_cls: Dict[str, Type[Dataset]] = {}

    def __init__(self, **datasets: Dataset):
        super().__init__(job_id=[])
        self.__datasets = datasets

    def __getitem__(self, key: str) -> Dataset:
        return self.__datasets[key]

    def to_dict(self):
        result = {}

        for name, dataset in self.__datasets.items():
            dataset_dict = dataset.to_dict()
            for k, v in dataset_dict.items():
                result[f"{name}:{k}"] = v

        return result

    @classmethod
    def _load(cls, data: Dict[str, Any], prefix: str = "") -> Dict[str, Any]:
        kwargs = {}
        for name, dataset_cls in cls._dataset_cls.items():
            full_prefix = f"{prefix}{name}:"
            dataset_kwargs = dataset_cls._load(data, prefix=full_prefix)

            kwargs[name] = dataset_cls(**dataset_kwargs)

        return kwargs

    @classmethod
    def configure(cls, **kwargs: Dict[str, Any]) -> None:
        for name, dataset_cls in cls._dataset_cls.items():
            if name in kwargs:
                dataset_cls.configure(**kwargs[name])

    @classmethod
    def get_latest_data_request(cls, date: datetime.datetime) -> List[ExportJobRequest]:
        result: Dict[Tuple[Union[datetime.datetime, None], Union[datetime.datetime, None]], ExportJobRequest] = {}
        for dataset_cls in cls._dataset_cls.values():
            cls_requests = dataset_cls.get_latest_data_request(date)
            for request in cls_requests:
                key = (
                    request.since if hasattr(request, "since") else None,
                    request.until if hasattr(request, "until") else None,
                )
                existing_request = result.get(key)
                if existing_request is not None:
                    existing_request.datasets.update(*request)
                else:
                    result[key] = request

        return list(result.values())

    @classmethod
    def create(cls, job_id: List[str], files: List[str]):
        kwargs: Dict[str, Dataset] = {}
        for name, dataset_cls in cls._dataset_cls.items():
            kwargs[name] = dataset_cls.create(job_id, files)

        return cls(**kwargs)

    async def update(self, latest_data: "Dataset", *, job_manager: JobManager = None) -> "Dataset":
        latest_data = cast(ComposedDataset, latest_data)

        tasks = []
        for name in type(self)._dataset_cls.keys():
            task = self.__datasets[name].update(latest_data.__datasets[name], job_manager=job_manager)
            tasks.append(task)

        await asyncio.gather(*tasks)

        return self

    @final
    @staticmethod
    def of(**kwargs: Type[Dataset]):
        def decorator(cls):
            cls._dataset_cls = kwargs
            return cls

        return decorator
