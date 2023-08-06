import gc
import json
import os
import warnings

import pandas as pd
import pyspark

warnings.filterwarnings('always')
warnings.filterwarnings('ignore')

from spark_datax_schema_tools.utils.utils import clean_df
from spark_datax_schema_tools.utils.utils import reformat_mask
from spark_datax_schema_tools.utils.utils import extract_only_parentesis
from spark_datax_schema_tools.utils.utils import extract_split_partitions
from spark_datax_schema_tools.utils.utils import spark_schema_structure2, spark_schema_structure
from spark_datax_schema_tools.utils.utils import spark_transform_dtype
from spark_datax_schema_tools.utils.utils import transform_dtype
from spark_datax_schema_tools.utils.dictionary import schema_ddng_o
from spark_datax_schema_tools.utils.dictionary import schema_ddng_f
from spark_datax_schema_tools.utils.dictionary import apply_comparate_sofia_datum
from spark_datax_schema_tools.utils.dictionary import apply_boolean
from spark_datax_schema_tools.utils.dictionary import apply_internal_use
from spark_datax_schema_tools.utils.dictionary import read_table_summary
from spark_datax_schema_tools.utils.dictionary import ddng_object_sofia
from spark_datax_schema_tools.utils.dictionary import ddng_object_datum
from spark_datax_schema_tools.utils.dictionary import ddng_fields_sofia
from spark_datax_schema_tools.utils.dictionary import ddng_fields_datum
from spark_datax_schema_tools.utils.dataframe import show_spark_df
from spark_datax_schema_tools.utils.dataframe import show_pd_df
from spark_datax_schema_tools.utils.sofia import generate_sofia


def read_excel(path_excel=None,
               uuaa_name=None):
    if not path_excel:
        raise Exception(f'require var path_excel: {path_excel} ')

    if not uuaa_name:
        raise Exception(f'require var uuaa_name: {uuaa_name} ')

    try:
        df_summary = pd.read_excel(f'{path_excel}',
                                   usecols=["UUAA", "Table", "Frequency", "Partitions"],
                                   sheet_name='Summary', squeeze=True, engine='openpyxl')
        df_summary = df_summary.fillna(method='ffill', axis=0)
        df_summary.columns = ["uuaa", "table", "frequency", "partitions"]
        df_uuaa = pd.read_excel(f'{path_excel}', header=1, sheet_name=f'{uuaa_name}', engine='openpyxl')
    except:
        df_summary = pd.read_excel(f'{path_excel}',
                                   usecols=["UUAA", "Table"],
                                   sheet_name='Summary', squeeze=True)
        df_summary = df_summary.fillna(method='ffill', axis=0)
        df_summary["Frequency"] = ""
        df_summary["Partitions"] = ""
        df_summary.columns = ["uuaa", "table", "frequency", "partitions"]
        df_uuaa = pd.read_excel(f'{path_excel}', header=1, sheet_name=f'{uuaa_name}')

    lst = [list(df_uuaa.columns)]
    df_uuaa2 = pd.DataFrame(lst, columns=list(df_uuaa.columns))
    df_uuaa2.drop(df_uuaa2.columns[df_uuaa2.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
    df_uuaa2.columns = ['table', 'naming', 'logical_Name', 'descripcion', 'format', 'key', 'mandatory', 'calculated']

    lst = [list(df_uuaa.columns)]
    columns_header = ['table', 'naming', 'logical_Name', 'descripcion', 'format', 'key', 'mandatory', 'calculated']
    df_uuaa2 = pd.DataFrame(lst, columns=list(df_uuaa.columns))
    df_uuaa2.drop(df_uuaa2.columns[df_uuaa2.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
    df_uuaa2.columns = columns_header

    df_uuaa3 = df_uuaa.copy()
    df_uuaa3.drop(df_uuaa3.columns[df_uuaa3.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
    df_uuaa3.columns = columns_header

    df_uuaa4 = pd.concat([df_uuaa2, df_uuaa3], ignore_index=True)
    df_uuaa4["key"] = df_uuaa4["key"].apply(clean_df)
    df_uuaa4["mandatory"] = df_uuaa4["mandatory"].apply(clean_df)
    df_uuaa4["calculated"] = df_uuaa4["calculated"].apply(clean_df)

    del df_uuaa4["descripcion"]

    df = pd.merge(df_uuaa4, df_summary, how='left', on=['table'])
    df.reset_index(inplace=True)
    df['_dtype'] = df['format'].apply(transform_dtype)
    df['_partitions'] = df['partitions'].apply(extract_split_partitions)

    del df_summary, df_uuaa, df_uuaa2, df_uuaa3, df_uuaa4
    gc.collect()
    return df


def generate_schema_datax(df=None,
                          uuaa_name=None,
                          table_name=None,
                          schema_datax_version="0",
                          directory_output=None):
    if not isinstance(df, pd.DataFrame):
        raise Exception('require var df: {df} ')

    if not uuaa_name:
        raise Exception(f'require var uuaa_name: {uuaa_name} ')

    if not table_name:
        raise Exception(f'require var table_name: {table_name} ')

    if not schema_datax_version:
        raise Exception(f'require var schema_datax_version: {schema_datax_version} ')

    df = df[df["table"] == f'{table_name}']

    rs_dict = dict()
    for index, row in df.iterrows():
        table = str(row['table']).lower().strip()
        naming = str(row['naming']).lower().strip()
        _format = row['format']
        _mandatory = True if str(row['mandatory']).upper() == "YES" else False
        _dtype = row['_dtype']
        _format, _mask = reformat_mask(_format)

        if table not in rs_dict.keys():
            rs_dict[table] = dict(fields=list())

        table_name_split = table_name.split("_")
        table_name3 = "-".join(table_name_split[2:])
        schema_hdfs = f"schema-hdfs-{table_name3.lower()}-{schema_datax_version}"

        rs_dict[table]["_id"] = schema_hdfs
        rs_dict[table]["description"] = ""

        fields_dict = dict()
        fields_dict["name"] = naming
        fields_dict["type"] = eval(_dtype)
        fields_dict["logicalFormat"] = _format
        fields_dict["deleted"] = False
        fields_dict["metadata"] = False
        fields_dict["default"] = ""
        fields_dict["mask"] = _mask
        fields_dict["locale"] = "pe"
        fields_dict["mandatory"] = _mandatory
        rs_dict[table]["fields"].append(fields_dict)

    if not os.path.exists(f'{directory_output}/{table_name}'):
        os.makedirs(f'{directory_output}/{table_name}')

    with open(f'{directory_output}/{table_name}/schema_{table_name}.json', 'w') as f:
        json.dump(rs_dict[f"{table_name}"], f, indent=4)

    return rs_dict


def generate_metadata_spark(df=None,
                            table_name=None
                            ):
    if not isinstance(df, pd.DataFrame):
        raise Exception('require var df: {df} ')

    if not table_name:
        raise Exception(f'require var table_name: {table_name} ')

    from pyspark.sql import types

    df = df[df["table"] == f'{table_name}']

    struct_list = list()
    struct_list_string = list()
    for index, row in df.iterrows():
        naming = str(row['naming']).lower().strip()
        format = row['format']
        struct_list.append(spark_schema_structure(col=naming, format=format))
        struct_list_string.append(spark_schema_structure2(col=naming, format=format))
    p_schema = types.StructType(struct_list)
    p_schema_string = types.StructType(struct_list_string)

    return p_schema, p_schema_string


def generate_parquet_spark(spark=None,
                           df=None,
                           table_name=None,
                           spark_schema=None,
                           spark_schema_string=None,
                           directory_output=None,
                           sample_parquet=None,
                           columns_string_default={},
                           columns_date_default={},
                           columns_decimal_default={},
                           columns_integer_default={}
                           ):
    if not spark:
        raise Exception(f'require object spark: {spark} ')

    if not isinstance(df, pd.DataFrame):
        raise Exception('require var df: {df} ')

    if not table_name:
        raise Exception(f'require var table_name: {table_name} ')

    if not spark_schema:
        raise Exception(f'require var spark_schema: {spark_schema} ')

    import random
    import string
    from datetime import datetime
    from dateutil.relativedelta import relativedelta
    from faker import Faker
    from pyspark.sql import functions as func

    fake = Faker()

    df = df[df["table"] == f'{table_name}']

    output2 = list()
    for _ in range(sample_parquet):
        columns_dict = dict()

        for index, row in df.iterrows():
            naming = str(row['naming']).lower().strip()
            _format = row['format']
            _spark_format = spark_transform_dtype(format=_format)
            _parentheses = extract_only_parentesis(format=_format)

            _fake = None
            if _spark_format in ("INTEGER",):
                _fake = fake.pyint(min_value=0, max_value=9999)
                if naming in list(columns_integer_default.keys()):
                    new_int = int(columns_integer_default[naming])
                    _fake = fake.pyint(min_value=new_int, max_value=new_int)

            elif _spark_format in ("TIMESTAMP",):
                d2 = datetime.now()
                d1 = d2 - relativedelta(months=6)
                _fake = fake.date_time_between(start_date=d1, end_date=d2)
            elif _spark_format in ("DECIMAL",):
                _parentheses_split = str(_parentheses).split(",")
                if len(_parentheses_split) <= 1:
                    _decimal_left = int(_parentheses_split[0])
                    _decimal_right = 0
                else:
                    _decimal_left = int(_parentheses_split[0])
                    _decimal_right = int(_parentheses_split[1])

                min_value_left = int("1" * (_decimal_left - _decimal_right))
                max_value_left = int("9" * (_decimal_left - _decimal_right))

                if _decimal_right == 0:
                    _decimal_right2 = 1
                    min_value_right = int("0" * _decimal_right2)
                    max_value_right = int("0" * _decimal_right2)
                else:
                    _decimal_right2 = _decimal_right
                    min_value_right = int("1" * _decimal_right2)
                    max_value_right = int("9" * _decimal_right2)

                _fake = str(fake.pydecimal(left_digits=_decimal_left,
                                           right_digits=_decimal_right,
                                           positive=True,
                                           min_value=min_value_left,
                                           max_value=max_value_left))

                if naming in list(columns_decimal_default.keys()):
                    new_decimal = float(columns_decimal_default[naming])
                    _fake = fake.bothify(text=f'{new_decimal}')

            elif _spark_format in ("TIME",):
                _fake = fake.time()
            elif _spark_format in ("DATE",):
                if naming in list(columns_date_default.keys()):
                    new_text = columns_date_default[naming]
                    _fake = datetime.strptime(new_text, '%Y-%m-%d')
                else:
                    d2 = datetime.today()
                    d1 = d2 - relativedelta(months=6)
                    _fake = fake.date_between(start_date=d1, end_date=d2)
            elif _spark_format in ("STRING", "DATE"):
                if naming in ("g_entific_id",):
                    _fake = fake.bothify(text='PE')
                elif naming in ("gf_frequency_type", "frequency_type"):
                    _fake = fake.bothify(text='?', letters='DM')
                elif naming in list(columns_string_default.keys()):
                    new_text = columns_string_default[naming]
                    _fake = fake.bothify(text=new_text)
                else:
                    _fake = ''.join(random.choices(string.ascii_letters + string.digits, k=int(_parentheses)))
            columns_dict[naming] = _fake
        output2.append(columns_dict)
    df2 = pd.DataFrame(output2)

    df3 = spark.createDataFrame(df2, schema=spark_schema_string)

    for i in spark_schema.jsonValue()["fields"]:
        column_name = str(i["name"])
        column_type = str(i["type"])
        if column_type.startswith("decimal"):
            df3 = df3.withColumn(f"{column_name}", func.col(f"{column_name}").cast(f"{column_type}"))
        elif column_type.startswith("date"):
            df3 = df3.withColumn(f"{column_name}", func.col(f"{column_name}").cast("date"))
        elif column_type.startswith("timestamp"):
            df3 = df3.withColumn(f"{column_name}", func.col(f"{column_name}").cast("timestamp"))

    df3.coalesce(1).write.mode("overwrite").parquet(f'{directory_output}/{table_name}/dummy_{table_name}.parquet')

    return df3


def generate_components(spark=None,
                        path_excel=None,
                        uuaa_name=None,
                        table_name=None,
                        schema_datax_version="0",
                        directory_output="schema_dev_summary",
                        sample_parquet=500,
                        columns_string_default={},
                        columns_date_default={},
                        columns_decimal_default={},
                        columns_integer_default={}):
    df = read_excel(path_excel=path_excel, uuaa_name=uuaa_name)

    generate_schema_datax(df=df,
                          uuaa_name=uuaa_name,
                          table_name=table_name,
                          schema_datax_version=schema_datax_version,
                          directory_output=directory_output)

    spark_schema, spark_schema_string = generate_metadata_spark(df=df,
                                                                table_name=table_name)

    df2 = generate_parquet_spark(spark=spark,
                                 df=df,
                                 table_name=table_name,
                                 spark_schema=spark_schema,
                                 spark_schema_string=spark_schema_string,
                                 directory_output=directory_output,
                                 sample_parquet=sample_parquet,
                                 columns_string_default=columns_string_default,
                                 columns_date_default=columns_date_default,
                                 columns_decimal_default=columns_decimal_default,
                                 columns_integer_default=columns_integer_default
                                 )

    pyspark.sql.dataframe.DataFrame.show2 = show_spark_df
    pd.DataFrame.show2 = show_pd_df

    return df2


def generate_transmission_holding(spark=None,
                                  path_excel=None,
                                  uuaa_name=None,
                                  table_name=None,
                                  schema_datax_version="0",
                                  schema_write_or_read="write",
                                  frequency=None,
                                  group=None,
                                  solution_model=None,
                                  directory_output="schema_holding_datax"):
    if path_excel:
        df = read_excel(path_excel=path_excel, uuaa_name=uuaa_name)
        generate_schema_datax(df=df,
                              uuaa_name=uuaa_name,
                              table_name=table_name,
                              schema_datax_version=schema_datax_version,
                              directory_output=directory_output)

    generate_sofia(spark=spark,
                   uuaa_name=uuaa_name,
                   table_name=table_name,
                   schema_datax_version=schema_datax_version,
                   schema_write_or_read=schema_write_or_read,
                   frequency=frequency,
                   group=group,
                   solution_model=solution_model)


def generate_json_to_datax(spark=None,
                           path_json=None,
                           schema_datax_version="0",
                           directory_output="schema_json_to_datax"):
    import json

    datasset_json = path_json
    with open(datasset_json) as f:
        datax = json.load(f)

    rs_dict = dict()
    table_name = datax.get("_id", "")
    table_name_split = table_name.split("_")
    table_name3 = "-".join(table_name_split[2:])
    schema_hdfs = f"schema-hdfs-{table_name3.lower()}-{schema_datax_version}"

    rs_dict["_id"] = schema_hdfs
    rs_dict["description"] = datax.get("description", "")

    rs_list = list()
    for col in datax["fields"]:
        _mandatory = True if col.get('mandatory', False) == True else False
        _format = col.get("logicalFormat")
        _spark_format = spark_transform_dtype(format=_format)
        _format, _mask = reformat_mask(_format)

        fields_dict = dict()
        fields_dict["name"] = col.get("name", "")
        fields_dict["logicalFormat"] = col.get("logicalFormat", "")
        fields_dict["deleted"] = False
        fields_dict["metadata"] = False
        fields_dict["default"] = ""
        fields_dict["mask"] = _mask
        fields_dict["locale"] = "pe"
        fields_dict["date_type"] = _spark_format
        fields_dict["mandatory"] = _mandatory
        rs_list.append(fields_dict)

    rs_dict["fields"] = rs_list

    if not os.path.exists(f'{directory_output}/{table_name}'):
        os.makedirs(f'{directory_output}/{table_name}')

    with open(f'{directory_output}/{table_name}/schema_{table_name}.json', 'w') as f:
        json.dump(rs_dict, f, indent=4)


def generate_dictionary(spark=None,
                        path_excel=None,
                        uuaa_name=None,
                        table_name=None,
                        technical=None,
                        storage_zone="raw",
                        squad_name="skeleton_kappa",
                        directory_output="schema_dictionary"):
    df = read_excel(path_excel=path_excel, uuaa_name=uuaa_name)
    df_table_fields, fields_partitions = read_table_summary(df=df, table_name=table_name)

    if not os.path.exists(f'{directory_output}/{table_name}'):
        os.makedirs(f'{directory_output}/{table_name}')

    """Objects"""
    data_object_columns = schema_ddng_o()
    df_object_sofia = ddng_object_sofia(squad_name=squad_name,
                                        table_name=table_name,
                                        technical=technical,
                                        storage_zone=storage_zone,
                                        uuaa_name=uuaa_name,
                                        selected_columns=data_object_columns)

    df_object_datum = ddng_object_datum(squad_name=squad_name,
                                        table_name=table_name,
                                        technical=technical,
                                        storage_zone=storage_zone,
                                        uuaa_name=uuaa_name,
                                        selected_columns=data_object_columns)
    df_object_datum.columns = [f"NEW_{col}" for col in df_object_datum.columns]
    df_object_datum2 = df_object_datum.rename({"NEW_PHYSICAL_NAME_OBJECT": "PHYSICAL_NAME_OBJECT"}, axis=1)

    df_object_global = df_object_sofia.merge(df_object_datum2, on=['PHYSICAL_NAME_OBJECT'], how="left").fillna("")
    df_object_global["INICIATIVA"] = df_object_global.apply(lambda x: apply_comparate_sofia_datum(x["INICIATIVA"], x["NEW_INICIATIVA"]), axis=1)
    df_object_global["ESTADO"] = df_object_global.apply(lambda x: apply_comparate_sofia_datum(x["ESTADO"], x["NEW_ESTADO"]), axis=1)
    df_object_global["COMENTARIOS_DATA_MODELER_DEVELOPER"] = ""
    df_object_global["COMENTARIOS_ARQUITECTURA_LOCAL"] = ""
    df_object_global["COMENTARIOS_IKARA"] = ""
    df_object_global["PHYSICAL_NAME_OBJECT"] = df_object_global["PHYSICAL_NAME_OBJECT"]
    df_object_global["LOGICAL_NAME_OBJECT"] = df_object_global.apply(
        lambda x: apply_comparate_sofia_datum(x["LOGICAL_NAME_OBJECT"], x["NEW_LOGICAL_NAME_OBJECT"]), axis=1)
    df_object_global["DESCRIPTION_OBJECT"] = df_object_global.apply(
        lambda x: apply_comparate_sofia_datum(x["DESCRIPTION_OBJECT"], x["NEW_DESCRIPTION_OBJECT"]), axis=1)
    df_object_global["INFORMATION_GROUP_LEVEL_1"] = df_object_global.apply(
        lambda x: apply_comparate_sofia_datum(x["INFORMATION_GROUP_LEVEL_1"], x["NEW_INFORMATION_GROUP_LEVEL_1"]), axis=1)
    df_object_global["INFORMATION_GROUP_LEVEL_2"] = df_object_global.apply(
        lambda x: apply_comparate_sofia_datum(x["INFORMATION_GROUP_LEVEL_2"], x["NEW_INFORMATION_GROUP_LEVEL_2"]), axis=1)
    df_object_global["DATA_SOURCE_DS"] = df_object_global.apply(lambda x: apply_comparate_sofia_datum(x["DATA_SOURCE_DS"], x["NEW_DATA_SOURCE_DS"]),
                                                                axis=1)
    df_object_global["SECURITY_LEVEL"] = df_object_global.apply(lambda x: apply_comparate_sofia_datum(x["SECURITY_LEVEL"], x["NEW_SECURITY_LEVEL"]),
                                                                axis=1)
    df_object_global["ENCRYPTION_AT_REST"] = df_object_global.apply(
        lambda x: apply_comparate_sofia_datum(x["ENCRYPTION_AT_REST"], x["NEW_ENCRYPTION_AT_REST"]), axis=1)
    df_object_global["DEPLOYMENT_TYPE"] = df_object_global.apply(
        lambda x: apply_comparate_sofia_datum(x["DEPLOYMENT_TYPE"], x["NEW_DEPLOYMENT_TYPE"]), axis=1)
    df_object_global["MODEL_NAME"] = df_object_global.apply(lambda x: apply_comparate_sofia_datum(x["MODEL_NAME"], x["NEW_MODEL_NAME"]), axis=1)
    df_object_global["MODEL_VERSION"] = df_object_global.apply(lambda x: apply_comparate_sofia_datum(x["MODEL_VERSION"], x["NEW_MODEL_VERSION"]),
                                                               axis=1)
    df_object_global["OBJECT_VERSION"] = df_object_global.apply(lambda x: apply_comparate_sofia_datum(x["OBJECT_VERSION"], x["NEW_OBJECT_VERSION"]),
                                                                axis=1)
    df_object_global["TECHNICAL_RESPONSIBLE"] = df_object_global.apply(
        lambda x: apply_comparate_sofia_datum(x["TECHNICAL_RESPONSIBLE"], x["NEW_TECHNICAL_RESPONSIBLE"]), axis=1)
    df_object_global["STORAGE_TYPE"] = df_object_global.apply(lambda x: apply_comparate_sofia_datum(x["STORAGE_TYPE"], x["NEW_STORAGE_TYPE"]), axis=1)
    df_object_global["STORAGE_ZONE"] = df_object_global.apply(lambda x: apply_comparate_sofia_datum(x["STORAGE_ZONE"], x["NEW_STORAGE_ZONE"]), axis=1)
    df_object_global["DATA_PHYSICAL_PATH"] = df_object_global.apply(
        lambda x: apply_comparate_sofia_datum(x["DATA_PHYSICAL_PATH"], x["NEW_DATA_PHYSICAL_PATH"]), axis=1)
    df_object_global["UUAA"] = df_object_global.apply(lambda x: apply_comparate_sofia_datum(x["UUAA"], x["NEW_UUAA"]), axis=1)
    df_object_global["PARTITIONS"] = df_object_global.apply(lambda x: apply_comparate_sofia_datum(x["PARTITIONS"], x["NEW_PARTITIONS"]), axis=1)
    df_object_global["CURRENT_DEPTH"] = df_object_global.apply(lambda x: apply_comparate_sofia_datum(x["CURRENT_DEPTH"], x["NEW_CURRENT_DEPTH"]),
                                                               axis=1)
    df_object_global["REQUIRED_DEPTH"] = df_object_global.apply(lambda x: apply_comparate_sofia_datum(x["REQUIRED_DEPTH"], x["NEW_REQUIRED_DEPTH"]),
                                                                axis=1)
    df_object_global["STORAGE_TYPE_OF_SOURCE_OBJECT"] = df_object_global.apply(
        lambda x: apply_comparate_sofia_datum(x["STORAGE_TYPE_OF_SOURCE_OBJECT"], x["NEW_STORAGE_TYPE_OF_SOURCE_OBJECT"]), axis=1)
    df_object_global["PHYSICAL_NAME_OF_SOURCE_OBJECT"] = df_object_global.apply(
        lambda x: apply_comparate_sofia_datum(x["PHYSICAL_NAME_OF_SOURCE_OBJECT"], x["NEW_PHYSICAL_NAME_OF_SOURCE_OBJECT"]), axis=1)
    df_object_global["SOURCE_PATH"] = df_object_global.apply(lambda x: apply_comparate_sofia_datum(x["SOURCE_PATH"], x["NEW_SOURCE_PATH"]), axis=1)
    df_object_global["SOURCE_FILE_TYPE"] = df_object_global.apply(
        lambda x: apply_comparate_sofia_datum(x["SOURCE_FILE_TYPE"], x["NEW_SOURCE_FILE_TYPE"]), axis=1)
    df_object_global["SOURCE_FILE_DELIMITER"] = df_object_global.apply(
        lambda x: apply_comparate_sofia_datum(x["SOURCE_FILE_DELIMITER"], x["NEW_SOURCE_FILE_DELIMITER"]), axis=1)
    df_object_global["TARGET_FILE_TYPE"] = df_object_global.apply(
        lambda x: apply_comparate_sofia_datum(x["TARGET_FILE_TYPE"], x["NEW_TARGET_FILE_TYPE"]), axis=1)
    df_object_global["TARGET_FILE_DELIMITER"] = df_object_global.apply(
        lambda x: apply_comparate_sofia_datum(x["TARGET_FILE_DELIMITER"], x["NEW_TARGET_FILE_DELIMITER"]), axis=1)
    df_object_global["TAGS"] = df_object_global.apply(lambda x: apply_comparate_sofia_datum(x["TAGS"], x["NEW_TAGS"]), axis=1)
    df_object_global["MARK_OF_TACTICAL_OBJECT"] = df_object_global.apply(
        lambda x: apply_comparate_sofia_datum(x["MARK_OF_TACTICAL_OBJECT"], x["NEW_MARK_OF_TACTICAL_OBJECT"]), axis=1)
    df_object_global["SOURCE_DATABASE_ENGINE"] = df_object_global.apply(
        lambda x: apply_comparate_sofia_datum(x["SOURCE_DATABASE_ENGINE"], x["NEW_SOURCE_DATABASE_ENGINE"]), axis=1)
    df_object_global = df_object_global[data_object_columns]
    df_object_global.to_excel(f'{directory_output}/{table_name}/ddng_o.xlsx', index=False)

    """Fields"""
    data_fields_columns = schema_ddng_f()
    df_fields_sofia = ddng_fields_sofia(squad_name=squad_name,
                                        table_name=table_name,
                                        technical=technical,
                                        df_table_fields=df_table_fields,
                                        selected_columns=data_fields_columns)

    df_fields_datum = ddng_fields_datum(squad_name=squad_name,
                                        table_name=table_name,
                                        technical=technical,
                                        df_table_fields=df_table_fields,
                                        selected_columns=data_fields_columns)

    df_fields_datum.columns = [f"NEW_{col}" for col in df_fields_datum.columns]
    df_fields_datum2 = df_fields_datum.rename({"NEW_PHYSICAL_NAME_FIELD": "PHYSICAL_NAME_FIELD"}, axis=1)

    df_fields_global = df_fields_sofia.merge(df_fields_datum2, on=['PHYSICAL_NAME_FIELD'], how="left").fillna("")

    df_fields_global["INICIATIVA"] = df_fields_global.apply(lambda x: apply_comparate_sofia_datum(x["INICIATIVA"], x["NEW_INICIATIVA"]), axis=1)
    df_fields_global["ESTADO"] = df_fields_global.apply(lambda x: apply_comparate_sofia_datum(x["ESTADO"], x["NEW_ESTADO"]), axis=1)
    df_fields_global["COMENTARIOS_DATA_MODELER_DEVELOPER"] = ""
    df_fields_global["DEVOLVER_A_LOCAL"] = df_fields_global.apply(
        lambda x: apply_comparate_sofia_datum(x["DEVOLVER_A_LOCAL"], x["NEW_DEVOLVER_A_LOCAL"]), axis=1)
    df_fields_global["MOTIVO_LOCAL"] = ""
    df_fields_global["COMENTARIOS_ARQUITECTURA_LOCAL"] = ""
    df_fields_global["COMENTARIOS_IKARA"] = ""
    df_fields_global["JERARQUIA"] = ""
    df_fields_global["FORMATO_LOGICO_ARQUITECTURA"] = df_fields_global.apply(
        lambda x: apply_comparate_sofia_datum(x["FORMATO_LOGICO_ARQUITECTURA"], x["NEW_FORMATO_LOGICO_ARQUITECTURA"]), axis=1)
    df_fields_global["EXISTE_EN_REPO_CENTRAL"] = df_fields_global.apply(
        lambda x: apply_comparate_sofia_datum(x["EXISTE_EN_REPO_CENTRAL"], x["NEW_EXISTE_EN_REPO_CENTRAL"]), axis=1)
    df_fields_global["PHYSICAL_NAME_FIELD"] = df_fields_global.apply(
        lambda x: apply_comparate_sofia_datum(x["PHYSICAL_NAME_FIELD"], x["PHYSICAL_NAME_FIELD"]), axis=1)
    df_fields_global["LOGICAL_NAME_FIELD_SPA"] = df_fields_global.apply(
        lambda x: apply_comparate_sofia_datum(x["NEW_LOGICAL_NAME_FIELD_SPA"], x["LOGICAL_NAME_FIELD_SPA"]), axis=1)
    df_fields_global["SIMPLE_FIELD_DESCRIPTION_SPA"] = df_fields_global.apply(
        lambda x: apply_comparate_sofia_datum(x["NEW_SIMPLE_FIELD_DESCRIPTION_SPA"], x["SIMPLE_FIELD_DESCRIPTION_SPA"]), axis=1)
    df_fields_global["LEVEL"] = df_fields_global.apply(lambda x: apply_comparate_sofia_datum(x["LEVEL"], x["NEW_LEVEL"]), axis=1)
    df_fields_global["COMPLEX_STRUCTURE"] = df_fields_global.apply(
        lambda x: apply_comparate_sofia_datum(x["COMPLEX_STRUCTURE"], x["NEW_COMPLEX_STRUCTURE"]), axis=1)
    df_fields_global["TECHNICAL_COMMENTS"] = df_fields_global.apply(
        lambda x: apply_comparate_sofia_datum(x["TECHNICAL_COMMENTS"], x["NEW_TECHNICAL_COMMENTS"]), axis=1)
    df_fields_global["TOKENIZED_AT_DATA_SOURCE"] = df_fields_global.apply(
        lambda x: apply_comparate_sofia_datum(x["TOKENIZED_AT_DATA_SOURCE"], x["NEW_TOKENIZED_AT_DATA_SOURCE"]), axis=1)
    df_fields_global["DATA_TYPE"] = df_fields_global.apply(lambda x: apply_comparate_sofia_datum(x["DATA_TYPE"], x["NEW_DATA_TYPE"]), axis=1)
    df_fields_global["FORMAT"] = df_fields_global.apply(lambda x: apply_comparate_sofia_datum(x["FORMAT"], x["NEW_FORMAT"]), axis=1)
    df_fields_global["LOGICAL_FORMAT"] = df_fields_global.apply(lambda x: apply_comparate_sofia_datum(x["LOGICAL_FORMAT"], x["NEW_LOGICAL_FORMAT"]),
                                                                axis=1)
    df_fields_global["KEY"] = df_fields_global.apply(lambda x: apply_comparate_sofia_datum(x["KEY"], x["NEW_KEY"]), axis=1)
    df_fields_global["MANDATORY"] = df_fields_global.apply(lambda x: apply_comparate_sofia_datum(x["MANDATORY"], x["NEW_MANDATORY"]), axis=1)
    df_fields_global["DEFAULT_VALUE"] = df_fields_global.apply(lambda x: apply_comparate_sofia_datum(x["DEFAULT_VALUE"], x["NEW_DEFAULT_VALUE"]),
                                                               axis=1)
    df_fields_global["PHYSICAL_NAME_OF_SOURCE_OBJECT"] = df_fields_global.apply(
        lambda x: apply_comparate_sofia_datum(x["PHYSICAL_NAME_OF_SOURCE_OBJECT"], x["NEW_PHYSICAL_NAME_OF_SOURCE_OBJECT"]), axis=1)
    df_fields_global["SOURCE_FIELD"] = df_fields_global.apply(lambda x: apply_comparate_sofia_datum(x["SOURCE_FIELD"], x["NEW_SOURCE_FIELD"]), axis=1)
    df_fields_global["DATA_TYPE_OF_SOURCE_FIELD"] = df_fields_global.apply(
        lambda x: apply_comparate_sofia_datum(x["DATA_TYPE_OF_SOURCE_FIELD"], x["NEW_DATA_TYPE_OF_SOURCE_FIELD"]), axis=1)
    df_fields_global["FORMAT_OF_SOURCE_FIELD"] = df_fields_global.apply(
        lambda x: apply_comparate_sofia_datum(x["FORMAT_OF_SOURCE_FIELD"], x["NEW_FORMAT_OF_SOURCE_FIELD"]), axis=1)
    df_fields_global["FIELD_POSITION_IN_THE_OBJECT"] = df_fields_global.apply(
        lambda x: apply_comparate_sofia_datum(x["FIELD_POSITION_IN_THE_OBJECT"], x["NEW_FIELD_POSITION_IN_THE_OBJECT"]), axis=1)

    df_fields_global["GENERATED_FIELD"] = df_fields_global.apply(
        lambda x: apply_comparate_sofia_datum(x["NEW_GENERATED_FIELD"], x["GENERATED_FIELD"]), axis=1)
    df_fields_global["TOKENIZATION_TYPE"] = df_fields_global.apply(
        lambda x: apply_comparate_sofia_datum(x["NEW_TOKENIZATION_TYPE"], x["TOKENIZATION_TYPE"]), axis=1)
    df_fields_global["SECURITY_CLASS"] = df_fields_global.apply(lambda x: apply_comparate_sofia_datum(x["NEW_SECURITY_CLASS"], x["SECURITY_CLASS"]),
                                                                axis=1)
    df_fields_global["SECURITY_LABEL"] = df_fields_global.apply(lambda x: apply_comparate_sofia_datum(x["NEW_SECURITY_LABEL"], x["SECURITY_LABEL"]),
                                                                axis=1)
    df_fields_global["SECURITY_SUB_LABEL"] = df_fields_global.apply(
        lambda x: apply_comparate_sofia_datum(x["NEW_SECURITY_SUB_LABEL"], x["SECURITY_SUB_LABEL"]), axis=1)
    df_fields_global = df_fields_global[data_fields_columns]
    df_fields_global.to_excel(f'{directory_output}/{table_name}/ddng_f.xlsx', index=False)

    return df_fields_global
