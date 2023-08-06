# Pandas Manager
Pandas Manager is a Python module for quick manipulation with pandas dataframe.

## Usage
### Calculate AWS data type
* detect_aws_type
```python
from rcd_dev_kit.pandas_manager import detect_aws_type
detect_aws_type(df=my_dataframe)
```

### Data Check for data quality
* check_na
```python
from rcd_dev_kit.pandas_manager import check_na
check_na(df=my_dataframe, raise_error=True) # raise error if there is any NA
```

* check_duplication
```python
from rcd_dev_kit.pandas_manager import check_duplication
check_duplication(df=my_dataframe, lst_col=['col1', 'col2'], raise_error=True) # raise error if there is any duplicates
```
### Data convert for data consistency
* normalize_date_column
```python
from rcd_dev_kit.pandas_manager import normalize_date_column
normalize_date_column(df=my_dataframe, lst_date_col=["col1", "col2"], parse_format=None, display_format="%Y-%m-%d") # raise error if there is any NA
```
### normalize data
* strip_all_text_column
```python
from rcd_dev_kit.pandas_manager import strip_all_text_column
strip_all_text_column(df=my_dataframe) # strip all the str type columns in dataframe
```

## Roadmap
* add threshold for raising error.

## Feedback
Any questions or suggestions?
Please contact package maintainer **yu.levern@realconsultingdata.com**
