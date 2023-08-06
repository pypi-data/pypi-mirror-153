from codecs import open as codec_open


def read_sql(sql_file: str, **kwargs):
    """
    Returns formatted sql with given format map

    :param sql_file: relative location of sql file
    :param kwargs:
    :return: sql query as string
    """
    with codec_open(sql_file, "r", encoding="utf8") as f:
        if bool(kwargs):
            return f.read().format_map(kwargs)
        return f.read()
