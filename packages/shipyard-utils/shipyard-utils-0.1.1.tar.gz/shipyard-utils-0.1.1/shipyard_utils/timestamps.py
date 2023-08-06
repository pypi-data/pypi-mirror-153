from dateutil import parser
import os


def extract_from_timestamp(timestamp, time_part):
    """
    Extract the year, month, day, hour, minute, or second from a Shipyard generated timestamp.
    """
    datetime_timestamp = parser.parse(timestamp)
    if time_part in [
        'year',
        'YEAR',
        'Year',
        'Y',
        'YY',
        'YYYY',
        'y',
        'yy',
        'yyyy'
    ]:
        time_value = datetime_timestamp.year
    if time_part in ['month', 'MONTH', 'Month', 'M', 'MM']:
        time_value = datetime_timestamp.month
    if time_part in ['day', 'DAY', 'Day', 'D', 'DD', 'd', 'dd']:
        time_value = datetime_timestamp.day
    if time_part in [
        'hour',
        'HOUR',
        'Hour',
        'H',
        'HH',
        'h',
        'hh',
        'hr',
        'HR',
        'Hr'
    ]:
        time_value = datetime_timestamp.hour
    if time_part in [
        'minute',
        'MINUTE',
        'Minute',
        'm',
        'mm',
        'min',
        'MIN',
        'Min'
    ]:
        time_value = datetime_timestamp.minute
    if time_part in [
        'second',
        'SECOND',
        'Second',
        'S',
        'SS',
        's',
        'ss',
        'sec',
        'SEC',
        'Sec'
    ]:
        time_value = datetime_timestamp.second
    return str(time_value)


def set_extra_time_environment_variables():
    """
    Expand the existing set of Shipyard timestamp environment variables to include
    year, month, day, hour, minute, and second.
    """
    shipyard_elements = ['VESSEL', 'FLEET']
    time_types = ['START', 'SCHEDULED']

    for element in shipyard_elements:
        for time_type in time_types:
            datetime_object = parser.parse(
                os.environ.get(f'SHIPYARD_{element}_{time_type}_TIME'))
            os.environ[f'SHIPYARD_{element}_{time_type}_TIME_YEAR'] = str(
                datetime_object.year)
            os.environ[f'SHIPYARD_{element}_{time_type}_TIME_MONTH'] = str(
                datetime_object.month)
            os.environ[f'SHIPYARD_{element}_{time_type}_TIME_DAY'] = str(
                datetime_object.day)
            os.environ[f'SHIPYARD_{element}_{time_type}_TIME_HOUR'] = str(
                datetime_object.hour)
            os.environ[f'SHIPYARD_{element}_{time_type}_TIME_MINUTE'] = str(
                datetime_object.minute)
            os.environ[f'SHIPYARD_{element}_{time_type}_TIME_SECOND'] = str(
                datetime_object.second)
