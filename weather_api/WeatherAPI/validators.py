import datetime as dt

# Define 'datestring' function below which validates the input date value
# The input date value must be of the string format "YYYY-MM-DD".
# If the input string is in expected format, convert it into datetime object and return else
# else raise Value Error 'A Date in format, "%Y-%m-%d", is expected. '
def datestring(value):
    try:
        format= "%Y-%m-%d"
        dt_obj=dt.datetime.strptime(value, format)
        return dt_obj
    except ValueError:
        raise ValueError('A Date in format, "%Y-%m-%d", is expected. ')
