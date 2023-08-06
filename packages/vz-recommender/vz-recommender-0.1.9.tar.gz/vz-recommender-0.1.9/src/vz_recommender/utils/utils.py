import os
import json
import logging
from datetime import datetime
import pandas as pd
import boto3
import mlflow
import csv


def load_params(params_path):
    with open(params_path, "r") as f:
        params = json.load(f)
    params_flatten = pd.json_normalize(params, sep=".").to_dict(orient="records")[0]
    return params, params_flatten


def time2weekday(time):
    """
    0 -> 6
    Mon -> Sun
    """
    return int(datetime.fromisoformat(time).weekday())


def time2daytime(time):
    dt = datetime.fromisoformat(time)
    h = int(dt.hour)
    m = int(dt.minute)
    return 2 * h if m < 30 else 2 * h + 1


# def lookup_table_to_dict(table_path, idx_col, val_col, file_format="json"):
#     if file_format == "json":
#         lookup = pd.read_json(table_path, lines=True)
#     elif file_format == "csv":
#         lookup = pd.read_csv(table_path)
#     else:
#         raise NotImplementedError()
#     lookup_dict = lookup[[idx_col, val_col]].set_index(idx_col).to_dict()[val_col]
#     return lookup_dict

def lookup_table_to_dict(table_path, idx_col, val_col, file_format="json"):
    if file_format == "json":
        with open(table_path, "r") as file:
            lookup = json.load(file)
            lookup_dict = {
                lookup[idx_col][i]: lookup[val_col][i]
                for i in lookup[idx_col].keys()
            }
    elif file_format == "csv":
        with open(table_path, "r") as file:
            lookup_reader = csv.DictReader(file)
            lookup_dict = {}
            for row in lookup_reader:
                # idx_value = int(row[idx_col]) if row[idx_col].isdecimal() else row[idx_col]
                idx_value = row[idx_col]
                val_value = int(row[val_col]) if row[val_col].isdecimal() else row[val_col]
                lookup_dict.update({idx_value: val_value})
    else:
        raise NotImplementedError()
    return lookup_dict


def model_logging_setup(new_log_path, run_name, model_name, params_flatten):
    # WandB
    global wandb_run
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logging.basicConfig(
        filename=new_log_path,
        level=logging.INFO
    )

    # MLflow
    experiment_paths = [e.name for e in mlflow.list_experiments()]
    experiment_path = f"/MLflow/{model_name}"
    if experiment_path in experiment_paths:
        experiment_id = mlflow.get_experiment_by_name(name=experiment_path).experiment_id
    else:
        experiment_id = mlflow.create_experiment(name=experiment_path)
    return logger, experiment_id


class DownloadS3(object):
    def __init__(self, bucket, access_key, access_secret):
        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            level=logging.INFO,
        )
        self.logger = logging.getLogger("app_download")
        self.bucket = bucket
        self.access_key = access_key
        self.access_secret = access_secret
        self.data = None

    def download_folder(self, s3_prefix, local_dir):
        s3 = boto3.client('s3',
                          aws_access_key_id=self.access_key,
                          aws_secret_access_key=self.access_secret,
                          verify=False)
        list_obj = s3.list_objects_v2(Bucket=self.bucket, Prefix=s3_prefix)
        if list_obj["KeyCount"] > 1000:
            self.logger.error("Found more than 1000 keys and only read partial data")
        for content in list_obj["Contents"]:
            key = content["Key"]
            if not key.endswith("/"):
                path, filename = os.path.split(key)
                local_filepath = os.path.join(local_dir, filename)

                self.logger.info(key)
                self.logger.info(local_filepath)
                s3.download_file(self.bucket, key, local_filepath)
                self.logger.info("Download s3 {bucket}/{s3_path} to local {local_path}".format(bucket=self.bucket,
                                                                                          s3_path=key,
                                                                                          local_path=local_filepath))
        return None

    def download_single(self, s3_prefix, local_path, file_format="csv"):
        """
        Concat and download Databricks generated csv/json folder to local csv and rename it.
        """
        dfs = []
        keys = []
        s3 = boto3.client('s3',
                          aws_access_key_id=self.access_key,
                          aws_secret_access_key=self.access_secret,
                          verify=False)
        list_obj = s3.list_objects_v2(Bucket=self.bucket, Prefix=s3_prefix)
        if list_obj["KeyCount"] > 1000:
            self.logger.error("Found more than 1000 keys and only read partial data")
        for content in list_obj["Contents"]:
            if content["Key"].endswith(file_format):
                keys.append(content["Key"])
        self.logger.info("Found {n} {format} files from {bucket}/{dir}".format(n=len(keys), format=file_format,
                                                                          bucket=self.bucket, dir=s3_prefix))

        for key in keys:
            obj = s3.get_object(Bucket=self.bucket, Key=key)
            if file_format == "json":
                df = pd.read_json(obj["Body"], orient="columns", lines=True)
            elif file_format == "csv":
                df = pd.read_csv(obj["Body"])
            else:
                raise NotImplementedError()
            dfs.append(df)
        df = pd.concat(dfs)
        df.to_csv(local_path, index=False)
        self.logger.info("Save to {}".format(local_path))
        return None