# Dataclass Manager
Dataclass Manager is a Python module for organise different type of dataclass.
## Set up
Set up .env as follow:
```python
#mysql
MYSQL_HOST=x
MYSQL_DB=x
MYSQL_PORT=x
MYSQL_USER=x
MYSQL_PASSWORD=x
```
## Usage
### RawDataFile object
* RawDataFile
```python
from rcd_dev_kit.dataclass_manager import RawDataFile
class MyRawData(RawDataFile):
    source_name = "xxx"
    source_url = "xxx"
    source_uuid = "xxx"
    file_name = "xxx"
    file_folder = "xxx"

    def __init__(self):
        super().__init__(base_path=os.environ.get("MY_BASE_PATH"))
        # my attribute necessary
        self.xx = xx
        self.yy = yy

    def download(self):
        # my method to download raw data file

    def read(self):
        # my mehod to read RAW data of list of RAW data

    # other method necessary
```

## Roadmap


## Feedback
Any questions or suggestions?
Please contact package maintainer **yu.levern@realconsultingdata.com**
