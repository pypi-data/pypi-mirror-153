from datetime import datetime

def str_to_datetime(date_string):
    most_used_formats = ["%Y/%m/%d %H.%M.%S",
                         "%Y/%m/%d %H:%M:%S",
                         "%Y-%m-%d %H.%M.%S",
                         "%Y-%m-%d %H:%M:%S",
                         "%d/%m/%Y %H.%M.%S",
                         "%d/%m/%Y %H:%M:%S",
                         "%d-%m-%Y %H.%M.%S",
                         "%d-%m-%Y %H:%M:%S",
                         "%Y/%m/%d %H.%M",
                         "%Y/%m/%d %H:%M",
                         "%Y-%m-%d %H.%M",
                         "%Y-%m-%d %H:%M",
                         "%d/%m/%Y %H.%M",
                         "%d/%m/%Y %H:%M",
                         "%d-%m-%Y %H.%M",
                         "%d-%m-%Y %H:%M",
                         "%Y/%m/%d",
                         "%Y-%m-%d",
                         "%d/%m/%Y",
                         "%d-%m-%Y"]
    for format_ in most_used_formats:
        try:
            res = datetime.strptime(date_string, format_)
            return res
        except ValueError as e:
            continue
    raise ValueError("Formato data non supportato ({})".format(date_string))

def str_to_date(date_string):
    return str_to_datetime(date_string).date()
