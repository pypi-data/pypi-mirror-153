import datetime
from typing import List, cast
import numpy as np
from minder.dataset_manager._utils import Dataset
from minder.dataset_manager import Preprocessor
from minder.research_portal_client.models import ExportJobRequest, ExportJobRequestDataset
from minder.research_portal_client import JobManager


class UnlabelledUtiDataset(Dataset):
    attribute_map = {
        "activity": "activity",
        "patients": "patient_id",
        "dates": "dates",
    }

    def __init__(self, *, job_id: List[str], activity: np.ndarray, patients: np.ndarray, dates: np.ndarray):
        super().__init__(job_id=job_id)
        self.activity = activity
        self.patients = patients
        self.dates = dates

    @classmethod
    def get_latest_data_request(cls, date: datetime.datetime) -> List[ExportJobRequest]:
        today = datetime.datetime.combine(date.date(), datetime.time(0, 0), datetime.timezone.utc)
        last_sunday = today - datetime.timedelta(days=(date.weekday() + 7 + 1) % 7)
        sunday_a_week_ago = last_sunday - datetime.timedelta(days=7)

        return [
            ExportJobRequest(
                since=sunday_a_week_ago,
                until=last_sunday,
                common_observation_columns=["start_date", "patient_id"],
                omit_units=True,
                datasets={
                    "raw_door_sensor": ExportJobRequestDataset(columns=["location_name", "value"]),
                    "raw_appliance_use": ExportJobRequestDataset(columns=["location_name", "value"]),
                    "raw_activity_pir": ExportJobRequestDataset(columns=["location_name"]),
                },
            )
        ]

    @classmethod
    def create(cls, job_id: List[str], files: List[str]):
        preprocessor = Preprocessor(files)

        activity_data_df = preprocessor.load_activity_data()
        activity_data_df = preprocessor.standardise_activity_data(activity_data_df)

        activity_data_nd = preprocessor.reshape_activity_data(activity_data_df)
        _, patients, dates, _ = preprocessor.extract_data_from_index(activity_data_df.index)

        return cls(job_id=job_id, activity=activity_data_nd, patients=patients, dates=dates)

    async def update(self, latest_data: Dataset, *, job_manager: JobManager = None) -> "UnlabelledUtiDataset":
        await super().update(latest_data, job_manager=job_manager)

        latest_data = cast(UnlabelledUtiDataset, latest_data)

        update_start_date: datetime.date = min(latest_data.dates)
        mask = self.dates < update_start_date

        self.filter(mask)

        self.activity = np.concatenate([self.activity, latest_data.activity])
        self.patients = np.concatenate([self.patients, latest_data.patients])
        self.dates = np.concatenate([self.dates, latest_data.dates])

        return self

    def filter(self, mask: np.ndarray) -> "UnlabelledUtiDataset":
        self.activity = self.activity[mask]
        self.patients = self.patients[mask]
        self.dates = self.dates[mask]

        return self
