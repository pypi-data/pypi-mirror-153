import pandas as pd
import numpy as np
import os
from spark_datax_schema_tools.utils import BASE_DIR


def apply_comparate_sofia_datum(col1, col2):
    new_col = col1 or col2
    return new_col


def apply_boolean(col):
    if str(col).upper() in ("FALSE", False, "nan", np.nan, ""):
        new_col = False
    else:
        new_col = True
    return new_col


def apply_internal_use(col):
    if str(col).upper() in ("INTERNAL_USE", "nan", np.nan, ""):
        new_col = "INTERNAL_USE"
    else:
        new_col = "INTERNAL_USE"
    return new_col


def schema_ddng_o():
    ddng_o_dict = dict()
    ddng_o_list = list()

    ddng_o_dict["INICIATIVA"] = ""
    ddng_o_dict["ESTADO"] = "Aprobado"
    ddng_o_dict["COMENTARIOS_DATA_MODELER_DEVELOPER"] = ""
    ddng_o_dict["COMENTARIOS_ARQUITECTURA_LOCAL"] = ""
    ddng_o_dict["COMENTARIOS_IKARA"] = ""
    ddng_o_dict["PHYSICAL_NAME_OBJECT"] = ""
    ddng_o_dict["LOGICAL_NAME_OBJECT"] = ""
    ddng_o_dict["DESCRIPTION_OBJECT"] = ""
    ddng_o_dict["INFORMATION_GROUP_LEVEL_1"] = ""
    ddng_o_dict["INFORMATION_GROUP_LEVEL_2"] = ""
    ddng_o_dict["DATA_SOURCE_DS"] = ""
    ddng_o_dict["SECURITY_LEVEL"] = ""
    ddng_o_dict["ENCRYPTION_AT_REST"] = ""
    ddng_o_dict["DEPLOYMENT_TYPE"] = ""
    ddng_o_dict["MODEL_NAME"] = ""
    ddng_o_dict["MODEL_VERSION"] = ""
    ddng_o_dict["OBJECT_VERSION"] = ""
    ddng_o_dict["TECHNICAL_RESPONSIBLE"] = ""
    ddng_o_dict["STORAGE_TYPE"] = ""
    ddng_o_dict["STORAGE_ZONE"] = ""
    ddng_o_dict["DATA_PHYSICAL_PATH"] = ""
    ddng_o_dict["UUAA"] = ""
    ddng_o_dict["PARTITIONS"] = ""
    ddng_o_dict["CURRENT_DEPTH"] = ""
    ddng_o_dict["REQUIRED_DEPTH"] = ""
    ddng_o_dict["STORAGE_TYPE_OF_SOURCE_OBJECT"] = ""
    ddng_o_dict["PHYSICAL_NAME_OF_SOURCE_OBJECT"] = ""
    ddng_o_dict["SOURCE_PATH"] = ""
    ddng_o_dict["SOURCE_FILE_TYPE"] = ""
    ddng_o_dict["SOURCE_FILE_DELIMITER"] = ""
    ddng_o_dict["TARGET_FILE_TYPE"] = ""
    ddng_o_dict["TARGET_FILE_DELIMITER"] = ""
    ddng_o_dict["TAGS"] = ""
    ddng_o_dict["MARK_OF_TACTICAL_OBJECT"] = ""
    ddng_o_dict["SOURCE_DATABASE_ENGINE"] = ""
    ddng_o_list.append(ddng_o_dict)

    df = pd.DataFrame(ddng_o_list)
    data_object_columns = list(df.columns)

    return data_object_columns


def schema_ddng_f():
    ddng_f_dict = dict()
    ddng_f_list = list()

    ddng_f_dict["INICIATIVA"] = ""
    ddng_f_dict["ESTADO"] = ""
    ddng_f_dict["COMENTARIOS_DATA_MODELER_DEVELOPER"] = ""
    ddng_f_dict["DEVOLVER_A_LOCAL"] = ""
    ddng_f_dict["MOTIVO_LOCAL"] = ""
    ddng_f_dict["COMENTARIOS_ARQUITECTURA_LOCAL"] = ""
    ddng_f_dict["COMENTARIOS_IKARA"] = ""
    ddng_f_dict["JERARQUIA"] = ""
    ddng_f_dict["FORMATO_LOGICO_ARQUITECTURA"] = ""
    ddng_f_dict["EXISTE_EN_REPO_CENTRAL"] = ""
    ddng_f_dict["PHYSICAL_NAME_FIELD"] = ""
    ddng_f_dict["LOGICAL_NAME_FIELD_SPA"] = ""
    ddng_f_dict["SIMPLE_FIELD_DESCRIPTION_SPA"] = ""
    ddng_f_dict["LEVEL"] = ""
    ddng_f_dict["COMPLEX_STRUCTURE"] = ""
    ddng_f_dict["TECHNICAL_COMMENTS"] = ""
    ddng_f_dict["TOKENIZED_AT_DATA_SOURCE"] = ""
    ddng_f_dict["DATA_TYPE"] = ""
    ddng_f_dict["FORMAT"] = ""
    ddng_f_dict["LOGICAL_FORMAT"] = ""
    ddng_f_dict["KEY"] = ""
    ddng_f_dict["MANDATORY"] = ""
    ddng_f_dict["DEFAULT_VALUE"] = ""
    ddng_f_dict["PHYSICAL_NAME_OF_SOURCE_OBJECT"] = ""
    ddng_f_dict["SOURCE_FIELD"] = ""
    ddng_f_dict["DATA_TYPE_OF_SOURCE_FIELD"] = ""
    ddng_f_dict["FORMAT_OF_SOURCE_FIELD"] = ""
    ddng_f_dict["FIELD_POSITION_IN_THE_OBJECT"] = ""
    ddng_f_dict["GENERATED_FIELD"] = ""
    ddng_f_dict["TOKENIZATION_TYPE"] = ""
    ddng_f_dict["SECURITY_CLASS"] = ""
    ddng_f_dict["SECURITY_LABEL"] = ""
    ddng_f_dict["SECURITY_SUB_LABEL"] = ""

    ddng_f_list.append(ddng_f_dict)

    df = pd.DataFrame(ddng_f_list)
    data_fields_columns = list(df.columns)
    return data_fields_columns


def read_table_summary(df=None, table_name=None):
    from spark_datax_schema_tools import reformat_mask
    from spark_datax_schema_tools import spark_transform_dtype

    df2 = df[df["table"] == table_name]
    df2.reset_index(inplace=True, drop=True)
    df2["format2"] = df2["format"].apply(reformat_mask)
    df2["format_spark"] = df2["format"].apply(spark_transform_dtype)

    df2[['new_format', 'new_mask']] = pd.DataFrame([*df2.format2], df2.index).reset_index(drop=True)
    df2.columns = [str(col).upper().strip().replace(" ", "_") for col in df2.columns]
    df3 = df2.rename(columns={"KEY": "NEW_KEY", "MANDATORY": "NEW_MANDATORY", "_PARTITIONS": "NEW_PARTITION",
                              "NAMING": "PHYSICAL_NAME_FIELD"})

    df4 = df3.drop(["INDEX", "TABLE", "LOGICAL_NAME", "FORMAT", "FORMAT2", "CALCULATED", "UUAA",
                    "FREQUENCY", "_DTYPE", "NEW_PARTITION"], axis=1)
    df4['NEW_FIELD_POSITION'] = df4.index + 1

    fields_partitions = list(df3["PARTITIONS"].unique())
    if len(fields_partitions) > 0:
        fields_partitions = str(fields_partitions[0])
    else:
        fields_partitions = ""

    return df4, fields_partitions


def ddng_object_sofia(squad_name=None,
                      table_name=None,
                      technical=None,
                      storage_zone=None,
                      uuaa_name=None,
                      fields_partitions=None,
                      selected_columns=None,
                      ):
    file_path_name = os.path.join(BASE_DIR, "utils", "files", "sofia", "DDNG-O.xls")
    df = pd.read_excel(file_path_name)
    df.columns = [str(col).upper().strip().replace(" ", "_") for col in df.columns]
    df2 = df[df["STORAGE_TYPE"] == "HDFS-Parquet"].sort_values(["PHYSICAL_NAME_OBJECT", "STORAGE_ZONE"], ascending=[True, True])
    df3 = df2.drop_duplicates(["PHYSICAL_NAME_OBJECT", "LOGICAL_NAME_OBJECT"])
    df3 = df3[df3["PHYSICAL_NAME_OBJECT"] == table_name].fillna("")

    table2 = str(table_name).lower().split("_")[2:]
    table2 = "_".join(table2)

    df3["INICIATIVA"] = squad_name
    df3["ESTADO"] = "Aprobado"
    df3["COMENTARIOS_DATA_MODELER_DEVELOPER"] = ""
    df3["COMENTARIOS_ARQUITECTURA_LOCAL"] = ""
    df3["COMENTARIOS_IKARA"] = ""

    df3["PHYSICAL_NAME_OBJECT"] = df3["PHYSICAL_NAME_OBJECT"]
    df3["LOGICAL_NAME_OBJECT"] = ""
    df3["DESCRIPTION_OBJECT"] = ""
    df3["INFORMATION_GROUP_LEVEL_1"] = ""
    df3["INFORMATION_GROUP_LEVEL_2"] = ""

    df3["DATA_SOURCE_DS"] = ""
    df3["SECURITY_LEVEL"] = ""
    df3["ENCRYPTION_AT_REST"] = ""
    df3["DEPLOYMENT_TYPE"] = "Global-Implementation"

    df3["MODEL_NAME"] = df3["MODEL_NAME"]
    df3["MODEL_VERSION"] = df3["MODEL_VERSION"]
    df3["OBJECT_VERSION"] = df3["OBJECT_VERSION"]

    df3["TECHNICAL_RESPONSIBLE"] = technical
    df3["STORAGE_TYPE"] = "HDFS-Parquet"
    if storage_zone == "raw":
        df3["STORAGE_ZONE"] = "Rawdata"
        df3["SOURCE_PATH"] = f"/in/staging/datax/{uuaa_name.lower()}/x_write_{table2}_0_%%ODATE"
    elif storage_zone == "master":
        df3["STORAGE_ZONE"] = "Masterdata"
        df3["SOURCE_PATH"] = f"/in/raw/datax/{uuaa_name.lower()}/x_write_{table2}_0_%%ODATE"
    else:
        df3["STORAGE_ZONE"] = ""
        df3["SOURCE_PATH"] = ""

    df3["DATA_PHYSICAL_PATH"] = f"/data/{storage_zone.lower()}/{uuaa_name.lower()}/data/{table_name.lower()}"
    df3["UUAA"] = f"{uuaa_name.upper()}"
    df3["PARTITIONS"] = fields_partitions
    df3["CURRENT_DEPTH"] = df3["CURRENT_DEPTH"]
    df3["REQUIRED_DEPTH"] = ""
    df3["STORAGE_TYPE_OF_SOURCE_OBJECT"] = "HDFS-Parquet"
    df3["PHYSICAL_NAME_OF_SOURCE_OBJECT"] = f"x_write_hdfs_{table2}_0_%%ODATE"

    df3["SOURCE_FILE_TYPE"] = "Parquet"
    df3["SOURCE_FILE_DELIMITER"] = ""
    df3["TARGET_FILE_TYPE"] = "Parquet"
    df3["TARGET_FILE_DELIMITER"] = ""
    df3["TAGS"] = ""
    df3["MARK_OF_TACTICAL_OBJECT"] = "NO"
    df3["SOURCE_DATABASE_ENGINE"] = "HDFS-PARQUET"

    df3 = df3[selected_columns]
    return df3


def ddng_object_datum(squad_name=None,
                      table_name=None,
                      technical=None,
                      storage_zone=None,
                      uuaa_name=None,
                      fields_partitions=None,
                      selected_columns=None):
    file_path_name = os.path.join(BASE_DIR, "utils", "files", "datum", "Objects.csv")
    df = pd.read_csv(file_path_name, sep=";")
    df.columns = [str(col).upper().strip().replace(" ", "_") for col in df.columns]
    df2 = df[df["DESCRIPTION_OBJECT"] == "HDFS-Parquet"].sort_values(["OBJECT_ID", "STORAGE_TYPE"], ascending=[True, True])
    df3 = df2.drop_duplicates(["OBJECT_ID", "LOGICAL_NAME_OBJECT"])
    df3 = df3[df3["OBJECT_ID"] == table_name].fillna("")

    table2 = str(table_name).lower().split("_")[2:]
    table2 = "_".join(table2)

    df3["INICIATIVA"] = squad_name
    df3["ESTADO"] = "Aprobado"
    df3["COMENTARIOS_DATA_MODELER_DEVELOPER"] = ""
    df3["COMENTARIOS_ARQUITECTURA_LOCAL"] = ""
    df3["COMENTARIOS_IKARA"] = ""

    df3["PHYSICAL_NAME_OBJECT"] = df3["OBJECT_ID"]
    df3["LOGICAL_NAME_OBJECT"] = ""
    df3["DESCRIPTION_OBJECT"] = ""
    df3["INFORMATION_GROUP_LEVEL_1"] = df3["INFORMATIONAL_GROUP_LEVEL_1"]
    df3["INFORMATION_GROUP_LEVEL_2"] = df3["INFORMATIONAL_GROUP_LEVEL_2"]

    df3["DATA_SOURCE_DS"] = ""
    df3["SECURITY_LEVEL"] = ""
    df3["ENCRYPTION_AT_REST"] = ""
    df3["DEPLOYMENT_TYPE"] = "Global-Implementation"

    df3["MODEL_NAME"] = df3["MODEL_NAME"]
    df3["MODEL_VERSION"] = ""
    df3["OBJECT_VERSION"] = df3["SOURCE_DATA_MODEL_CODE"]

    df3["TECHNICAL_RESPONSIBLE"] = technical
    df3["STORAGE_TYPE"] = "HDFS-Parquet"
    if storage_zone == "raw":
        df3["STORAGE_ZONE"] = "Rawdata"
        df3["SOURCE_PATH"] = f"/in/staging/datax/{uuaa_name.lower()}/x_write_{table2}_0_%%ODATE"
    elif storage_zone == "master":
        df3["STORAGE_ZONE"] = "Masterdata"
        df3["SOURCE_PATH"] = f"/in/raw/datax/{uuaa_name.lower()}/x_write_{table2}_0_%%ODATE"
    else:
        df3["STORAGE_ZONE"] = ""
        df3["SOURCE_PATH"] = ""

    df3["DATA_PHYSICAL_PATH"] = f"/data/{storage_zone.lower()}/{uuaa_name.lower()}/data/{table_name.lower()}"
    df3["UUAA"] = f"{uuaa_name.upper()}"
    df3["PARTITIONS"] = fields_partitions
    df3["CURRENT_DEPTH"] = ""
    df3["REQUIRED_DEPTH"] = ""
    df3["STORAGE_TYPE_OF_SOURCE_OBJECT"] = ""
    df3["PHYSICAL_NAME_OF_SOURCE_OBJECT"] = f"x_write_hdfs_{table2}_0_%%ODATE"

    df3["SOURCE_FILE_TYPE"] = "Parquet"
    df3["SOURCE_FILE_DELIMITER"] = ""
    df3["TARGET_FILE_TYPE"] = "Parquet"
    df3["TARGET_FILE_DELIMITER"] = ""
    df3["TAGS"] = ""
    df3["MARK_OF_TACTICAL_OBJECT"] = "NO"
    df3["SOURCE_DATABASE_ENGINE"] = "HDFS-PARQUET"

    df3 = df3[selected_columns]
    return df3


def ddng_fields_sofia(squad_name=None,
                      table_name=None,
                      technical=None,
                      df_table_fields=None,
                      selected_columns=None):
    file_path_name = os.path.join(BASE_DIR, "utils", "files", "sofia", "DDNG-F.xls")
    df = pd.read_excel(file_path_name)
    df.columns = [str(col).strip().replace(" ", "_") for col in df.columns]
    df['PHYSICAL_NAME_FIELD'] = df['PHYSICAL_NAME_FIELD'].str.lower()

    df2 = df.sort_values(["PHYSICAL_NAME_FIELD", "REGISTRATION_DATE"], ascending=[True, True])
    df3 = df2.drop_duplicates(["PHYSICAL_NAME_FIELD", "LOGICAL_NAME_FIELD"]).fillna("")

    fields_columns = df_table_fields["PHYSICAL_NAME_FIELD"].values.tolist()
    df4 = df3[df3["PHYSICAL_NAME_FIELD"].isin(fields_columns)].reset_index(drop=True)

    df5 = df_table_fields.merge(df4, on=['PHYSICAL_NAME_FIELD'], how="left").fillna("")

    table2 = str(table_name).lower().split("_")[2:]
    table2 = "_".join(table2)

    df5["INICIATIVA"] = squad_name
    df5["ESTADO"] = "Aprobado"
    df5["COMENTARIOS_DATA_MODELER_DEVELOPER"] = ""
    df5["DEVOLVER_A_LOCAL"] = "N"
    df5["MOTIVO_LOCAL"] = ""
    df5["COMENTARIOS_ARQUITECTURA_LOCAL"] = ""
    df5["COMENTARIOS_IKARA"] = ""
    df5["JERARQUIA"] = ""
    df5["FORMATO_LOGICO_ARQUITECTURA"] = df5["NEW_FORMAT"]
    df5["EXISTE_EN_REPO_CENTRAL"] = "SI"
    df5["PHYSICAL_NAME_FIELD"] = df5["PHYSICAL_NAME_FIELD"]
    df5["LOGICAL_NAME_FIELD_SPA"] = df5["LOGICAL_NAME_FIELD_(SPA)"]
    df5["SIMPLE_FIELD_DESCRIPTION_SPA"] = df5["SIMPLE_FIELD_DESCRIPTION_(SPA)"]
    df5["LEVEL"] = df5["LEVEL"]
    df5["COMPLEX_STRUCTURE"] = df5["COMPLEX_STRUCTURE"]
    df5["TECHNICAL_COMMENTS"] = technical
    df5["TOKENIZED_AT_DATA_SOURCE"] = ""
    df5["DATA_TYPE"] = df5["FORMAT_SPARK"]
    df5["FORMAT"] = df5["NEW_MASK"]
    df5["LOGICAL_FORMAT"] = df5["NEW_FORMAT"]
    df5["KEY"] = df5["NEW_KEY"]
    df5["MANDATORY"] = df5["NEW_MANDATORY"]
    df5["DEFAULT_VALUE"] = df5["DEFAULT_VALUE"]
    df5["PHYSICAL_NAME_OF_SOURCE_OBJECT"] = f"x_write_hdfs_{table2}_0_%%ODATE"
    df5["SOURCE_FIELD"] = df5["PHYSICAL_NAME_FIELD"]
    df5["DATA_TYPE_OF_SOURCE_FIELD"] = df5["FORMAT_SPARK"]
    df5["FORMAT_OF_SOURCE_FIELD"] = df5["NEW_MASK"]
    df5["FIELD_POSITION_IN_THE_OBJECT"] = df5["NEW_FIELD_POSITION"]

    df5["GENERATED_FIELD"] = df5["GENERATED_FIELD"].apply(apply_boolean)
    df5["TOKENIZATION_TYPE"] = df5["TOKENIZATION_TYPE"].apply(apply_boolean)

    df5["SECURITY_CLASS"] = df5["SECURITY_CLASS"].apply(apply_internal_use)
    df5["SECURITY_LABEL"] = df5["SECURITY_LABEL"].apply(apply_internal_use)
    df5["SECURITY_SUB_LABEL"] = ""
    df5 = df5[selected_columns]
    return df5


def ddng_fields_datum(squad_name=None,
                      table_name=None,
                      technical=None,
                      df_table_fields=None,
                      selected_columns=None):
    file_path_name = os.path.join(BASE_DIR, "utils", "files", "datum", "Fields.csv")
    df = pd.read_csv(file_path_name, sep=";")
    df.columns = [str(col).upper().strip().replace(" ", "_") for col in df.columns]
    df['PHYSICAL_NAME_FIELD'] = df['PHYSICAL_NAME_FIELD'].str.lower()

    df2 = df.sort_values(["PHYSICAL_NAME_FIELD", "REGISTRATION_DATE"], ascending=[True, True])
    df3 = df2.drop_duplicates(["PHYSICAL_NAME_FIELD", "LOGICAL_NAME_FIELD"]).fillna("")

    fields_columns = df_table_fields["PHYSICAL_NAME_FIELD"].values.tolist()
    df4 = df3[df3["PHYSICAL_NAME_FIELD"].isin(fields_columns)].reset_index(drop=True)

    df5 = df_table_fields.merge(df4, on=['PHYSICAL_NAME_FIELD'], how="left")

    table2 = str(table_name).lower().split("_")[2:]
    table2 = "_".join(table2)

    df5["INICIATIVA"] = squad_name
    df5["ESTADO"] = "Aprobado"
    df5["COMENTARIOS_DATA_MODELER_DEVELOPER"] = ""
    df5["DEVOLVER_A_LOCAL"] = "N"
    df5["MOTIVO_LOCAL"] = ""
    df5["COMENTARIOS_ARQUITECTURA_LOCAL"] = ""
    df5["COMENTARIOS_IKARA"] = ""
    df5["JERARQUIA"] = ""
    df5["FORMATO_LOGICO_ARQUITECTURA"] = df5["NEW_FORMAT"]
    df5["EXISTE_EN_REPO_CENTRAL"] = "SI"
    df5["PHYSICAL_NAME_FIELD"] = df5["PHYSICAL_NAME_FIELD"]
    df5["LOGICAL_NAME_FIELD_SPA"] = df5["LOGICAL_NAME_FIELD"]
    df5["SIMPLE_FIELD_DESCRIPTION_SPA"] = df5["DESCRIPTION_FIELD"]
    df5["LEVEL"] = ""
    df5["COMPLEX_STRUCTURE"] = ""
    df5["TECHNICAL_COMMENTS"] = technical
    df5["TOKENIZED_AT_DATA_SOURCE"] = ""
    df5["DATA_TYPE"] = df5["FORMAT_SPARK"]
    df5["FORMAT"] = df5["NEW_MASK"]
    df5["LOGICAL_FORMAT"] = df5["NEW_FORMAT"]
    df5["KEY"] = df5["NEW_KEY"]
    df5["MANDATORY"] = df5["NEW_MANDATORY"]
    df5["DEFAULT_VALUE"] = df5["DEFAULT_VALUE"]
    df5["PHYSICAL_NAME_OF_SOURCE_OBJECT"] = f"x_write_hdfs_{table2}_0_%%ODATE"
    df5["SOURCE_FIELD"] = df5["PHYSICAL_NAME_FIELD"]
    df5["DATA_TYPE_OF_SOURCE_FIELD"] = df5["FORMAT_SPARK"]
    df5["FORMAT_OF_SOURCE_FIELD"] = df5["NEW_MASK"]
    df5["FIELD_POSITION_IN_THE_OBJECT"] = df5["NEW_FIELD_POSITION"]

    df5["GENERATED_FIELD"] = df5["GENERATED_FIELD"].apply(apply_boolean)
    df5["TOKENIZATION_TYPE"] = df5["TOKENIZED_AT_DATASOURCE"].apply(apply_boolean)

    df5["SECURITY_CLASS"] = df5["SECURITY_CLASS"].apply(apply_internal_use)
    df5["SECURITY_LABEL"] = df5["SECURITY_LABEL"].apply(apply_internal_use)
    df5["SECURITY_SUB_LABEL"] = ""

    df5 = df5[selected_columns]
    return df5
