import datetime
import logging
from typing import Dict, List, Tuple, Union
import numpy as np
import pandas as pd
import os


logger = logging.getLogger(__name__)


class Preprocessor(object):
    def __init__(self, files: List[str]):
        self.__files = files

    def load_activity_data(self) -> pd.DataFrame:
        dataset_names = ["raw_door_sensor", "raw_appliance_use", "raw_activity_pir"]
        col_filter = ["patient_id", "start_date", "location_name", "value"]

        activity_dataset: pd.DataFrame = None
        for dataset_name in dataset_names:
            dataset = self.__load_dataset(dataset_name)
            dataset = dataset.loc[dataset.start_date != "start_date"]

            if dataset_name == "raw_appliance_use":
                dataset.location_name = dataset.value.apply(lambda x: x.split("-")[0])

            dataset["value"] = 1
            dataset = dataset[col_filter]
            dataset.columns = ["id", "time", "location", "value"]
            dataset.time = pd.to_datetime(dataset.time, utc=True).dt.tz_convert(None)

            activity_dataset = pd.concat([activity_dataset, dataset], ignore_index=True, copy=False)

        return activity_dataset

    def load_uti_labels(self, manual_labels: pd.DataFrame = None) -> Dict[Tuple[str, datetime.date], bool]:
        procedures: pd.DataFrame = self.__load_dataset("procedure")
        if procedures is None:
            raise __PreprocessorError(message="Procedures dataset not present")

        def uti_filter(x):
            texts = [str(x.type), str(x.notes)]
            keywords = ["urine", "urinalysis", "uti"]

            for text in texts:
                for keyword in keywords:
                    if keyword in text:
                        return True

            return False

        procedures.notes = procedures.notes.apply(lambda x: str(x).lower())
        procedures.type = procedures.type.apply(lambda x: str(x).lower())

        mask = procedures.apply(uti_filter, axis=1)
        procedures = procedures.loc[mask, ["patient_id", "start_date", "outcome", "notes"]]
        procedures.columns = ["patient id", "date", "valid", "notes"]

        outcome_mapping: Dict[str, Union[bool, None]] = {
            "http://snomed.info/sct|260385009": False,  # Negative
            "http://snomed.info/sct|10828004": True,  # Positive
            "http://snomed.info/sct|82334004": None,  # Indeterminate
        }

        def map_outcome(x):
            mapped = outcome_mapping.get(x.valid)
            return "negative" not in x.notes if mapped else mapped

        procedures.valid = procedures.apply(map_outcome, axis=1)
        procedures = procedures[["patient id", "date", "valid"]]
        procedures.date = pd.to_datetime(procedures.date).dt.date
        procedures.dropna(inplace=True)

        if manual_labels is not None:
            procedures = pd.concat([procedures, manual_labels], ignore_index=True, copy=False)

        procedures.drop_duplicates(inplace=True)

        procedures.set_index(["patient id", "date"], inplace=True)
        return procedures["valid"].to_dict()

    def expand_uti_labels(
        self,
        labels: Dict[Tuple[str, datetime.date], bool],
        days_either_side: int = 0,
    ) -> Dict[Tuple[str, datetime.date], bool]:
        if days_either_side == 0:
            return labels

        label_df = pd.DataFrame(
            labels.values(),
            index=pd.MultiIndex.from_tuples(labels.keys(), names=["patient_id", "date"]),
            columns=["valid"],
        )
        label_df.reset_index(inplace=True)

        def dates_either_side_group_by(x):
            date = pd.to_datetime(x["date"].values[0])
            x = [x] * (2 * days_either_side + 1)
            new_date_values = np.arange(-days_either_side, days_either_side + 1)
            new_dates = [(date + datetime.timedelta(int(value))).date() for value in new_date_values]
            x = pd.concat(x)
            x["date"] = new_dates
            return x

        return (
            label_df.groupby(["patient_id", "date", "valid"])
            .apply(dates_either_side_group_by)
            .reset_index(drop=True)
            .set_index(["patient_id", "date"])["valid"]
            .to_dict()
        )

    def apply_uti_labels(
        self,
        unlabelled_df: pd.DataFrame,
        uti_labels: Dict[Tuple[str, datetime.date], bool],
    ) -> pd.DataFrame:
        dropIndex = unlabelled_df.index.names != ["id", "date"]
        if dropIndex:
            dropDate = "date" not in unlabelled_df.columns
            if dropDate:
                unlabelled_df["date"] = unlabelled_df.time.dt.date

            unlabelled_df.set_index(["id", "date"], drop=False, inplace=True)

        unlabelled_df["valid"] = unlabelled_df.index.map(uti_labels)

        if dropIndex:
            unlabelled_df.reset_index(drop=True, inplace=True)

            if dropDate:
                unlabelled_df.drop(columns=["date"], inplace=True)

        return unlabelled_df

    def standardise_activity_data(
        self,
        df: pd.DataFrame,
        *,
        uti_labels: Dict[Tuple[str, datetime.date], bool] = None,
        drop_time: bool = True,
    ) -> pd.DataFrame:
        df.drop_duplicates(inplace=True, ignore_index=True)
        df.loc[:, "date"] = df.time.dt.date

        df_start = df[["id", "date", "location"]].drop_duplicates()
        df_start["time"] = pd.to_datetime(df_start.date)
        df_end = df_start.copy()
        df_end.time += datetime.timedelta(hours=23)

        df = pd.concat([df, df_start, df_end], sort=False, ignore_index=True, copy=False)
        df.drop_duplicates(subset=["id", "time", "location"], inplace=True)
        df.fillna(0.0, inplace=True)

        df = df.groupby(["id", "location"]).apply(lambda x: x.set_index("time").resample("H").sum()).reset_index()
        table_df = df.pivot_table(index=["id", "time"], columns="location", values="value").reset_index()
        table_df.fillna(0.0, inplace=True)

        sensors = [
            "back door",
            "bathroom1",
            "bedroom1",
            "dining room",
            "fridge door",
            "front door",
            "hallway",
            "kettle",
            "kitchen",
            "living room",
            "lounge",
            "microwave",
            "study",
            "toaster",
        ]
        for sensor in sensors:
            if sensor not in table_df.columns:
                table_df[sensor] = 0.0

        table_df.dropna(inplace=True)
        table_df["date"] = table_df.time.dt.date
        table_df = table_df[["id", "date"] + (["time"] if not drop_time else []) + sensors]
        table_df.set_index(["id", "date"], inplace=True)

        if uti_labels is not None:
            table_df = self.apply_uti_labels(table_df, uti_labels)
            table_df.set_index(["valid"], append=True, inplace=True)

        return table_df

    def reshape_activity_data(self, df: pd.DataFrame) -> np.ndarray:
        if "time" in df.columns:
            df.drop(columns="time", inplace=True)

        return df.to_numpy().reshape(-1, 24, len(df.columns))

    def extract_data_from_index(
        self, index: pd.MultiIndex
    ) -> Tuple[pd.MultiIndex, np.ndarray, np.ndarray, Union[np.ndarray, None]]:
        """
        Extract values for each index level.

        Parameters
        ----------
        index : MultiIndex from a standartised datasest. Optianally with labels applied to it.

        Returns
        -------
        Tuple(indices, patient_ids, dates, labels)

        Labels will be None if index did not contain labels.
        """
        indices: pd.MultiIndex = index.drop_duplicates()
        patient_ids = indices.get_level_values(0).astype(str).to_numpy()
        dates = indices.get_level_values(1).to_numpy()
        labels = indices.get_level_values(2).astype(int).to_numpy() if indices.nlevels == 3 else None
        return (indices, patient_ids, dates, labels)

    def split_labeled(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Split the DataFrame into labelled and unlabelled data.

        Split the DataFrame based on 3rd level of its index:
            - `isna() == True` will be in unlabelled data frame
            - the rest will be in the labelled data frame

        Parameters
        ----------
        df : DataFrame with a standartised datasest. Optianally with labels applied to it.
            If no labels are applied, entire DataFrame is treated an unlabelled.

        Returns
        -------
        Tuple of DataFrame or None with 2 elements: labelled and unlabelled.
        """
        if df.index.nlevels != 3:
            return (None, df)

        groups = df.groupby(df.index.get_level_values(2).isna())
        split = [x for _, x in groups]
        if len(split) == 2:
            return (split[0], split[1])

        return (None, split[0]) if pd.isna(df.index[0][2]) else (split[0], None)

    def __load_dataset(self, dataset: str) -> pd.DataFrame:
        concat_csv: pd.DataFrame = None
        for file_path in self.__files:
            filename = os.path.basename(file_path)
            file_dataset = filename.split("-")[0]
            if file_dataset != dataset:
                continue

            csv_content = pd.read_csv(file_path, index_col=False, memory_map=True)
            concat_csv = pd.concat([concat_csv, csv_content], ignore_index=True, copy=False)

        if concat_csv is not None:
            concat_csv.drop_duplicates(inplace=True, ignore_index=True)

        return concat_csv


class __PreprocessorError(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        """Custom error messages for exception"""
        return self.message
