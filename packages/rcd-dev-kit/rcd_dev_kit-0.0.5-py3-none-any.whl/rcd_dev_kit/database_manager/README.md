# Database Manager
Database Manager is a Python module for manipulating data with different databases.

## Set up
Set up .env as follow:
```python
#elasticsearch
ELASTICSEARCH_SCHEME=x
ELASTICSEARCH_PORT=x
ELASTICSEARCH_HOST=x
ELASTICSEARCH_USER=x
ELASTICSEARCH_PASSWORD=x

#redshift
REDSHIFT_HOST=x
REDSHIFT_USER=x
REDSHIFT_PASSWORD=x
REDSHIFT_DB=x

#S3
S3_BUCKET_DEV=x
S3_BUCKET_RAW=x
S3_BUCKET_DATAMART=x
AWS_ACCESS_KEY_ID=x
AWS_SECRET_ACCESS_KEY=x
AWS_DEFAULT_REGION=x

#Gcloud
GOOGLE_APPLICATION_CREDENTIALS=x
OPEN_DATA_SOURCE_BUCKET=x
GCLOUD_PROJECT=x
```

## Usage
### Elasticsearch
* index_json_bulk_parallel
```python
import pandas as pd
from rcd_dev_kit import database_manager
# bulk indexing data to elasticsearch
database_manager.index_json_bulk_parallel(index_name="my_index_name", method="json", json_path='my_json_path', keyword="") # with json file
database_manager.index_json_bulk_parallel(index_name="my_index_name", method="dataframe", df=my_dataframe) # with pandas dataframe, pass your dataframe by pd_dataframe
```
* index_json_bulk
```python
database_manager.index_json_bulk(json_path="my_json_path", index_name="my_index_name", keyword="") # bulk indexing data to elasticsearch
```

* index_json
```python
database_manager.index_json(json_path="my_json_path", index_name="my_index_name", keyword="") # indexing data to elasticsearch
```

### Redshift
* send_to_redshift
```python
import pandas as pd
database_manager.send_to_redshift(database="my_database", schema="test_schema", table="my_table_name", df=my_dataframe) # fast way to send data to redshift&s3 without checking consistency
database_manager.send_to_redshift(database="my_database", schema="test_schema", table="my_table_name", df=my_dataframe, check=True) # slow way to send data to redshift&s3 but will table structure
```
* read_from_redshift
```python
database_manager.read_from_redshift(database="my_database", method="auto", schema="my_schema", table="my_table_name", debug=True) # reading data from redshift with auto mode
database_manager.read_from_redshift(database="my_database", method="sql", sql_query='SELECT * FROM reference.jp__gender_dictionary__mhlw', debug=False) # reading data from redshift with sql query
```
### S3
* upload_raw_s3
```python
database_manager.upload_raw_s3(local_folder_path="my_folder", uuid="my_uuid")
```
* download_raw_s3
```python
database_manager.download_raw_s3(local_folder_path="my_folder", uuid="my_uuid")
```
### Gcloud storage
* upload_to_gcloud
```python
database_manager.upload_to_gcloud(local_folder_path="my_folder", uuid="my_uuid")
```
* download_from_gcloud
```python
database_manager.download_from_gcloud(local_folder_path="my_folder", uuid="my_uuid")
```
## Roadmap
* Redshift: Find package for calculating significant digits of precision.
* Redshift: Dynamically adding or deleting columns.
* Redshift: Transfer sqlalchemy core to sqlalchemy orm.


## Feedback
Any questions or suggestions?
Please contact package maintainer **yu.levern@realconsultingdata.com**
