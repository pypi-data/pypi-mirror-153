import os
from typing import List
from google.cloud import storage
from ..decorator_manager import timeit
from ..file_manager import detect_all_files, detect_path


@timeit(program_name="Upload data folder to gcloud")
def upload_to_gcloud(
    local_folder_path: str,
    uuid: str,
    bucket: str = os.environ.get("OPEN_DATA_SOURCE_BUCKET"),
):
    """
    Function upload_to_gcloud.
    Upload raw data folder to gcloud.

    Parameters:
          local_folder_path (str): The path of local folder which contains files.
          uuid (str): The uuid for the source.
          bucket (str, default env var "OPEN_DATA_SOURCE_BUCKET"): The bucket on gcloud to access data.

    Examples:
        >>> from rcd_dev_kit import database_manager
        >>> database_manager.upload_to_gcloud(local_folder_path="my_folder", uuid="my_uuid")
    """
    os.path.isdir(local_folder_path)
    uuid_path = os.path.join(local_folder_path.split(uuid)[0], uuid)
    sub_folder_path = local_folder_path.split(uuid)[1]

    gcs = GcloudOperator(bucket=bucket)
    lst_blob = [
        path
        for blob in gcs.list_blob(prefix=f"{uuid}{sub_folder_path}")
        if (path := blob.name.removeprefix(f"{uuid}/")) != ""
    ]
    print(f"💧{len(lst_blob)} blob from `{bucket}/{uuid}{sub_folder_path}` detected.")
    lst_local_file = [
        file_path.removeprefix(f"{uuid_path}{os.path.sep}")
        for file_path in detect_all_files(local_folder_path, full_path=True)
        if not os.path.split(file_path)[-1].startswith(".")
    ]
    print(f"📑{len(lst_local_file)} local files from `{local_folder_path}` detected.")
    lst_upload = sorted(
        [file_path for file_path in set(lst_local_file) - set(lst_blob)]
    )
    print(f"📤{len(lst_upload)} local file need to be uploaded as gcloud blob.")

    for file_path in lst_upload:
        gcs.upload_blob(
            local_file_path=os.path.join(uuid_path, file_path),
            blob_path=os.path.join(uuid, file_path),
        )


@timeit(program_name="download data folder from gcloud")
def download_from_gcloud(
    local_folder_path: str,
    uuid: str,
    bucket: str = os.environ.get("OPEN_DATA_SOURCE_BUCKET"),
):
    """
    Function download_from_gcloud.
    Download raw data folder from gcloud.

    Parameters:
          local_folder_path(str): The path of local folder which contains files.
          uuid(str): The uuid for the source.
          bucket (str, default env var "OPEN_DATA_SOURCE_BUCKET"): The bucket on gcloud to access data.

    Examples:
        >>> from rcd_dev_kit import database_manager
        >>> database_manager.download_from_gcloud(local_folder_path="my_folder", uuid="my_uuid")
    """
    detect_path(local_folder_path)
    uuid_path = os.path.join(local_folder_path.split(uuid)[0], uuid)
    sub_folder_path = local_folder_path.split(uuid)[1]

    gcs = GcloudOperator(bucket=bucket)
    lst_blob = [
        path
        for blob in gcs.list_blob(prefix=f"{uuid}{sub_folder_path}")
        if (path := blob.name.removeprefix(f"{uuid}/")) != ""
    ]
    print(f"💧{len(lst_blob)} blob from `{bucket}/{uuid}{sub_folder_path}` detected.")

    lst_local_file = [
        file_path.removeprefix(f"{uuid_path}{os.path.sep}")
        for file_path in detect_all_files(local_folder_path, full_path=True)
        if not os.path.split(file_path)[-1].startswith(".")
    ]

    print(f"📑{len(lst_local_file)} local files from `{local_folder_path}` detected.")
    lst_download = sorted(
        [file_path for file_path in set(lst_blob) - set(lst_local_file)]
    )
    print(f"📥{len(lst_download)} gcloud blob need to be downloaded as local file.")

    for file_path in lst_download:
        gcs.download_blob(
            local_file_path=os.path.join(uuid_path, file_path),
            blob_path=os.path.join(uuid, file_path),
        )

class GcloudOperator:
    def __init__(self, bucket: str = os.environ.get("OPEN_DATA_SOURCE_BUCKET")) -> None:
        self.client = storage.Client()
        self.bucket = self.client.get_bucket(bucket)
        print(f"☑️Bucket is set to: {self.bucket}")

    def list_blob(self, prefix: str) -> List:
        return [blob for blob in self.bucket.list_blobs(prefix=prefix)]

    def download_blob(self, local_file_path: str, blob_path: str) -> None:
        blob = self.bucket.get_blob(blob_path)

        dir_to_make = "/".join(local_file_path.split("/")[:-1])
        if not os.path.exists(dir_to_make):
            os.makedirs(dir_to_make)

        with open(local_file_path, "wb") as file_obj:
            blob.download_to_file(file_obj)

    def upload_blob(self, local_file_path: str, blob_path: str) -> None:
        blob = self.bucket.blob(blob_path)
        blob.upload_from_filename(filename=local_file_path)
