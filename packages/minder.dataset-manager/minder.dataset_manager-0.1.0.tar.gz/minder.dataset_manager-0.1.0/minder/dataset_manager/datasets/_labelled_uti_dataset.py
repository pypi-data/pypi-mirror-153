import datetime
from functools import cached_property
from typing import List, cast
from minder.dataset_manager._utils import Dataset, ComposedDataset
from minder.dataset_manager.datasets import UtiLabelsDataset, UnlabelledUtiDataset
from minder.research_portal_client.models import ExportJobRequest
from minder.research_portal_client import JobManager
import pandas as pd


@ComposedDataset.of(activity=UnlabelledUtiDataset, uti_labels=UtiLabelsDataset)
class LabelledUtiDataset(ComposedDataset):
    def __init__(self, *, activity: UnlabelledUtiDataset, uti_labels: UtiLabelsDataset):
        super().__init__(activity=activity, uti_labels=uti_labels)
        mask = ~self.labels.isna()
        activity.filter(mask)
        try:
            delattr(self, "labels")
        except AttributeError:
            pass

    @cached_property
    def labels(self):
        activity: UnlabelledUtiDataset = self["activity"]
        uti_labels: UtiLabelsDataset = self["uti_labels"]
        return pd.MultiIndex.from_arrays([activity.patients, activity.dates]).map(uti_labels.labels)

    @classmethod
    def get_latest_data_request(cls, date: datetime.datetime) -> List[ExportJobRequest]:
        label_request = cls._dataset_cls["label"].get_latest_data_request(date)[0]
        activity_request = cls._dataset_cls["activity"].get_latest_data_request(date)[0]
        activity_request.datasets.update(label_request.datasets)
        activity_request.since = label_request.since
        activity_request.until = label_request.until

        return [activity_request]

    async def update(self, latest_data: Dataset, *, job_manager: JobManager = None) -> "LabelledUtiDataset":
        latest_data = cast(LabelledUtiDataset, latest_data)
        latest_activity = cast(UnlabelledUtiDataset, latest_data["activity"])
        latest_labels = cast(UtiLabelsDataset, latest_data["uti_labels"])

        earliest_label = min(pd.MultiIndex.from_tuples(latest_labels.labels.keys()).get_level_values(1))
        earliest_data = min(latest_activity.dates)

        # Need to download previous job
        if earliest_label < earliest_data:
            if job_manager is None:
                raise ValueError("job_manager not provided")

            previous_job_id = self["activity"]._job_id[-1]
            files = await Dataset.download([previous_job_id], job_manager)
            previous_dataset = UnlabelledUtiDataset.create(previous_job_id, files)

            mask = (previous_dataset.dates >= earliest_label) & (previous_dataset.dates < earliest_data)
            previous_dataset.filter(mask)
            missing_labelled = LabelledUtiDataset(activity=previous_dataset, uti_labels=latest_labels)

            await super().update(missing_labelled, job_manager=job_manager)

        await super().update(latest_data, job_manager=job_manager)

        try:
            delattr(self, "labels")
        except AttributeError:
            pass

        return self
