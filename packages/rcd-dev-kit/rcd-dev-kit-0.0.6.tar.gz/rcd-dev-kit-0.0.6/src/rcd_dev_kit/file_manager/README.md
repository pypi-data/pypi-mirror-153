# File Manager
File Manager is a Python module for manipulating directory and files.

## Usage
### File detector
* detect_path
```python
from rcd_dev_kit import file_manager
file_manager.detect_path(path="my_path")
```
>👉🏻Path "my_path" does not exist, creating...

>🥂Path "my_path" exists.
* detect_all_files
```python
from rcd_dev_kit import file_manager
file_manager.detect_all_files(root_path="my_path")
```
>['.DS_Store', '2021-10-13---bdmit__cip_ampp_list.json', 'test.xlsx', 'cip_ampp_code.csv']
```python
file_manager.detect_all_files(root_path="my_path", full_path=True)
```
>['tmp/.DS_Store', 'tmp/2021-10-13---bdmit__cip_ampp_list.json', 'tmp/test.xlsx', 'tmp/hello/cip_ampp_code.csv']

### File writer
```python
from rcd_dev_kit import file_manager
file_manager.write_df_to_json_parallel(df=my_dataframe, json_path="my_path")
```
>✅'Parallel Writing pd.DataFrame to json' end in 0:00:00.008030 s.⏰
### File operator (in dev)
* FileOperator
```python
from rcd_dev_kit import file_manager
fo = file_manager.FileOperator("price_tracker/all/drug_cards")
fo.remove_all()
```
>Initializing directory path as 'price_tracker/all/drug_cards'
> 
>There are 84651 files under directory.


## Roadmap
* add detect file suffix
* add detect file size
* add rename file
* add docs

## Feedback
Any questions or suggestions?
Please contact package maintainer **yu.levern@realconsultingdata.com**
