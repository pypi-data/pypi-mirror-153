import datetime
from typing import Dict, List, Tuple, cast
from minder.dataset_manager._utils import Dataset
from minder.dataset_manager import Preprocessor
from minder.research_portal_client.models import ExportJobRequest, ExportJobRequestDataset
from minder.research_portal_client import JobManager
import numpy as np


class UtiLabelsDataset(Dataset):
    attribute_map = {
        "labels": "label",
    }

    __expand_labels: int = 1

    def __init__(self, *, job_id: List[str], labels: np.ndarray):
        super().__init__(job_id=job_id)
        self.labels = cast(Dict[Tuple[str, datetime.date], bool], labels.flat[0])

    @classmethod
    def configure(cls, **kwargs) -> None:
        cls.__configure(**kwargs)

    @classmethod
    def __configure(cls, *, expand_labels: int):
        cls.__expand_labels = expand_labels

    @classmethod
    def get_latest_data_request(cls, date: datetime.datetime) -> List[ExportJobRequest]:
        today = datetime.datetime.combine(date.date(), datetime.time(0, 0), datetime.timezone.utc)
        last_sunday = today - datetime.timedelta(days=(date.weekday() + 7 + 1) % 7)
        sunday_a_week_ago = last_sunday - datetime.timedelta(days=7)
        sunday_2_weeks_ago = sunday_a_week_ago - datetime.timedelta(days=7)

        return [
            ExportJobRequest(
                since=sunday_2_weeks_ago,
                until=sunday_a_week_ago,
                datasets={
                    "procedure": ExportJobRequestDataset(
                        columns=["start_date", "type", "patient_id", "outcome", "notes"]
                    )
                },
            )
        ]

    @classmethod
    def create(cls, job_id: List[str], files: List[str]):
        preprocessor = Preprocessor(files)
        labels = preprocessor.load_uti_labels()
        labels = preprocessor.expand_uti_labels(labels, cls.__expand_labels)

        return cls(job_id=job_id, labels=np.asarray(labels))

    async def update(self, latest_data: "Dataset", *, job_manager: JobManager = None) -> "UtiLabelsDataset":
        await super().update(latest_data, job_manager=job_manager)

        latest_data = cast(UtiLabelsDataset, latest_data)

        self.labels.update(latest_data.labels)

        return self
