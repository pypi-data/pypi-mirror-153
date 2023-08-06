def extract_only_parentesis(format):
    import re
    _number = re.findall(r'\(.*?\)', format)
    if len(_number) > 0:
        res = str(_number[0])
        res = res.replace("(", "").replace(")", "").strip()
    else:
        res = ""
    return res


def extract_only_column_text(col):
    import re
    new_col = str(col).lower()

    _text = re.findall(r'([a-zA-Z ]+)', new_col)
    if len(_text) > 0:
        res = _text[0]
    else:
        res = ""
    return res


def transform_dtype(col):
    new_col = str(col).lower()
    text = str(extract_only_column_text(col)).upper()

    if text == "TIMESTAMP":
        _type = "['timestamp', 'null']"
    elif text == "DECIMAL":
        _type = f"['null', '{new_col}']"
    elif text == "TIME":
        _type = "['string', 'null']"
    elif text == "DATE":
        _type = "['date', 'null']"
    elif text in ("NUMERIC SHORT", "INTEGER"):
        _type = "['null', 'int32']"
    else:
        _type = "['string', 'null']"
    return _type


def spark_transform_dtype(format):
    text = str(extract_only_column_text(format)).upper()

    if text in ("NUMERIC SHORT", "INTEGER"):
        _type = "INTEGER"
    elif text in ("TIMESTAMP",):
        _type = "TIMESTAMP"
    elif text in ("DECIMAL",):
        _type = "DECIMAL"
    elif text in ("TIME",):
        _type = "STRING"
    elif text in ("DATE",):
        _type = "DATE"
    else:
        _type = "STRING"
    return _type


def spark_schema_structure(col, format):
    from pyspark.sql import types

    _dtype = spark_transform_dtype(format)
    _parentheses = extract_only_parentesis(format)

    if _dtype == "INTEGER":
        _type = types.StructField(col, types.IntegerType())
    elif _dtype == "TIMESTAMP":
        _type = types.StructField(col, types.TimestampType())
    elif _dtype == "DECIMAL":
        _parentheses_split = str(_parentheses).split(",")

        # if len(_parentheses_split) <= 1:
        #     _decimal_left_digits = int(_parentheses_split[0])
        #     if _decimal_left_digits >= 23:
        #         _decimal_left = 23
        #         _decimal_right = 10
        #     else:
        #         _decimal_left = _decimal_left_digits
        #         _decimal_right = 0
        # else:
        #     _decimal_left_digits = int(_parentheses_split[0])
        #     _decimal_right_digits = int(_parentheses_split[1])
        #     if _decimal_left_digits >= 23:
        #         _decimal_left = 23
        #         _decimal_right = 10
        #     elif _decimal_left_digits < _decimal_right_digits:
        #         _decimal_left = _decimal_left_digits
        #         _decimal_right = 3
        #     else:
        #         _decimal_left = _decimal_left_digits
        #         _decimal_right = _decimal_right_digits

        if len(_parentheses_split) <= 1:
            _decimal_left = int(_parentheses_split[0])
            _decimal_right = 0
        else:
            _decimal_left = int(_parentheses_split[0])
            _decimal_right = int(_parentheses_split[1])

        _type = types.StructField(col, types.DecimalType(precision=_decimal_left, scale=_decimal_right))

    elif _dtype == "TIME":
        _type = types.StructField(col, types.StringType())
    elif _dtype == "DATE":
        _type = types.StructField(col, types.DateType())
    else:
        _type = types.StructField(col, types.StringType())

    return _type


def spark_schema_structure2(col, format):
    from pyspark.sql import types

    _dtype = spark_transform_dtype(format)
    _parentheses = extract_only_parentesis(format)

    if _dtype == "INTEGER":
        _type = types.StructField(col, types.IntegerType())
    elif _dtype == "TIMESTAMP":
        _type = types.StructField(col, types.TimestampType())
    elif _dtype == "DECIMAL":
        _type = types.StructField(col, types.StringType())

    elif _dtype == "TIME":
        _type = types.StructField(col, types.StringType())
    elif _dtype == "DATE":
        _type = types.StructField(col, types.DateType())
    else:
        _type = types.StructField(col, types.StringType())

    return _type


def reformat_mask(_format):
    if str(_format).upper() == "DATE":
        _mask = "yyyy-MM-dd"
    elif str(_format).upper() == "TIMESTAMP":
        _mask = "yyyy-MM-dd HH:mm:ss.SSSSSS"
    elif str(_format).upper() == "TIME":
        _mask = ""
        _format = "ALPHANUMERIC(8)"
    else:
        _mask = ""

    return _format, _mask


def extract_split_partitions(col):
    new_col = str(col).split(";")
    if len(new_col) > 0:
        res = f"{new_col}"
    else:
        res = "[]"
    return res


def clean_df(col):
    new_col = str(col).strip()
    if str(new_col) in ("YES.1", "YES.2", "YES.3", "YES"):
        res = "YES"
    else:
        res = "NO"
    return res
