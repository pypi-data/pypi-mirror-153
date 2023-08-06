def generate_sofia(spark=None,
                   uuaa_name=None,
                   table_name=None,
                   schema_datax_version=None,
                   schema_write_or_read=None,
                   frequency=None,
                   group=None,
                   solution_model=None):
    import pandas as pd
    import os
    from prettytable import PrettyTable
    from spark_datax_schema_tools.utils import BASE_DIR

    if not uuaa_name:
        raise Exception(f'require var uuaa_name:{uuaa_name} ')

    if not table_name:
        raise Exception(f'require var table_name:{table_name} ')

    if not schema_datax_version:
        raise Exception(f'require var table_version:{schema_datax_version} ')

    frequency_list = ["daily", "monthly"]
    if not frequency:
        raise Exception(f'require var frequency:{frequency} ')
    else:
        if str(frequency) not in frequency_list:
            raise Exception(f'variable frequency only in {frequency_list}')

    group_list = ["CIB", "CLIENT_SOLUTIONS", "CORE_BANKING", "GLOBAL_DATA", "RISK_FINANCE"]
    if not group:
        raise Exception(f'require var frequency:{group} ')
    else:
        if str(group) not in group_list:
            raise Exception(f'variable group only in {group_list}')

    solution_model_list = ["CIB", "CDD"]
    if not solution_model:
        raise Exception(f'require var solution_model:{solution_model} ')
    else:
        if str(solution_model) not in solution_model_list:
            raise Exception(f'variable solution_model only in {solution_model_list}')

    file_path_name = os.path.join(BASE_DIR, "utils", "files", "sofia", "DDNG-O.xls")
    file_path_name2 = os.path.join(BASE_DIR, "utils", "files", "datum", "Objects.xls")
    df = pd.read_excel(file_path_name)
    df2 = pd.read_excel(file_path_name2)
    df.columns = [str(col).upper().strip().replace(" ", "_") for col in df.columns]
    df2.columns = [str(col).upper().strip().replace(" ", "_") for col in df2.columns]

    df_sofia = df[df["PHYSICAL_NAME_OBJECT"] == f'{table_name}']
    df_datum = df2[df2["PHYSICAL_NAME_OBJECT"] == f'{table_name}']
    description_name = "Required Description"
    logical_name = "Required Logical Name"
    if df_sofia.shape[0] > 0:
        description_name = df_datum["DESCRIPTION_OBJECT"].values[0]
        logical_name = df_sofia["LOGICAL_NAME_OBJECT"].values[0]

    if schema_write_or_read == "write":
        text_schema = "Write"
        text_connection = "in"
    elif schema_write_or_read == "read":
        text_schema = "Read"
        text_connection = "out"

    uuaa = f"{uuaa_name.upper()}"
    table_name_split = table_name.split("_")
    table_name2 = "_".join(table_name_split[2:])
    table_name3 = "-".join(table_name_split[2:])
    schema_datax_version = f"{schema_datax_version.lower()}"
    adapter_hdfs = f"adapter-hdfs-{uuaa.lower()}-{text_connection}"
    schema_hdfs = f"schema-hdfs-{table_name3.lower()}-{schema_datax_version}"

    _frequency = frequency
    _group = group
    solution_model = "CDD"
    if solution_model == "CDD":
        solution_link = "https://drive.google.com/file/d/190yMMLyMe_10eAF2PBUeNeB0dimEhNcD/view"
    elif solution_model == "CIB":
        solution_link = "https://drive.google.com/file/d/13iHMC-_q-TDe-QuVMIy_PWtuI_7Vfxvs/view"

    t = PrettyTable()
    t.field_names = [f"Adapter {text_schema}", "Value", ]
    t.add_row(["Adapter_id", f"{adapter_hdfs.lower()}"])
    t.add_row(["Adapter_description", f"Adapter to {text_schema} HDFS in UUAA {uuaa.upper()}"])
    t.add_row(["Adapter_system_or_driver", "hdfs.v2"])
    t.add_row(["Connection_id", f"con-pe-{uuaa.lower()}-hdfs-{text_connection}"])
    t.add_row(["Connection_description", f"Connection to {text_schema} HDFS in UUAA {uuaa.upper()}"])
    t.add_row(["Connection_system", "//datax.work-02/ns/ecs.datax/systems/hdfs.v2"])
    if schema_write_or_read == "read":
        t.add_row(["Connection_basepath", f"/data/master/{uuaa.lower()}/data"])
    else:
        t.add_row(["Connection_basepath", f"/in/staging/datax/{uuaa.lower()}"])
    t.add_row(["Connection_tenant", "pe"])
    print(t)

    t = PrettyTable()
    t.field_names = [f"Schema {text_schema}", "Value", ]
    t.add_row(["Schema_id", f"{schema_hdfs}"])
    t.add_row(["Schema_description", f"{description_name}"])
    t.add_row(["Fraud enablers", "False"])
    t.add_row(["Sensitive personal information", "False"])
    t.add_row(["Personal_identification", "False"])
    t.add_row(["Information for internal", "False"])
    t.add_row(["Nomenclature", "False"])
    t.add_row(["upload json", f"schema_{table_name}.json"])
    print(t)

    t = PrettyTable()
    t.field_names = [f"DataObject {text_schema}", "Value"]
    t.add_row(["GENERAL_INFO", f""])
    t.add_row(["------------", f""])
    t.add_row(["Dataobject_id", f"x_{text_schema.lower()}_hdfs_{table_name2}_{schema_datax_version}"])
    t.add_row(["Dataobject_description", f"{description_name}"])
    t.add_row(["Dataobject_direction", f"{text_schema.upper()}"])
    t.add_row(["Adapter_namespace", f"(WORK-02) pe.{uuaa.lower()}.app-id-xxxx.dev"])
    t.add_row(["Adapter_type", f"{adapter_hdfs.upper()}"])
    if schema_write_or_read == "read":
        t.add_row(["QueryParamas_paths", f"{table_name.lower()}"])
        t.add_row(["sqlfilter", f"gf_cutoff_date=" + "'{CUTOFF_DATE}'"])
        t.add_row(["Parameter", "CUTOFF_DATE - STRING - YYYY-MM-DD"])
    else:
        t.add_row(["QueryParamas_paths", f"x_{text_schema.lower()}_hdfs_{table_name2}_0" + "_{ODATE}"])
        t.add_row(["sqlfilter", ""])
        t.add_row(["Parameter", "ODATE - STRING - YYYYMMDD"])

    t.add_row(["kirby version", "2"])
    t.add_row(["size", "L"])
    t.add_row(["Format", "PARQUET"])
    t.add_row([f"", f""])
    t.add_row(["SCHEMA_INFO", f""])
    t.add_row(["-----------", f""])
    t.add_row(["Namespace", f"(WORK-02) pe.{uuaa.lower()}.app-id-xxxx.dev"])
    t.add_row(["Schema", f"{schema_hdfs.upper()}"])
    t.add_row([f"", f""])
    t.add_row(["METADATA_INFO", f""])
    t.add_row(["-------------", f""])
    t.add_row(["Logical_Name", f"{logical_name}"])
    t.add_row(["uuaa", f"{uuaa.upper()}"])
    t.add_row(["TypeObject", "TABLE"])
    t.add_row(["Frecuency", f"{_frequency}"])
    t.add_row(["NumEstimatedRecord", f"1000000"])
    t.add_row(["ValidationGroup", f"{_group.upper()}"])
    t.add_row(["Momenclature", f"TC-015"])
    t.add_row(["StorageType", f"HDFS-PARQUET"])
    t.add_row(["DataSystem", f"{_group.lower()}"])
    t.add_row(["CompanyName", f"BBVA PERU"])
    print(t)

    t = PrettyTable()
    t.field_names = [f"Transfer {text_schema}", "Value"]
    t.add_row(["GENERAL_INFO", f""])
    t.add_row(["------------", f""])
    t.add_row(["Transfer_id", f"p{uuaa.lower()}_hdfs_hdfs_{table_name2}_{schema_datax_version}"])
    t.add_row(["Transfer_description", f"{description_name}"])
    t.add_row(["SolucionModel", f"{solution_link}"])
    t.add_row(["Source Namespace", f"(WORK-01) gl.{uuaa.lower()}.app-id-xxxx.dev"])
    t.add_row(["Source Dataobject", f"x_t_{table_name2}_{schema_datax_version}"])
    t.add_row(["Destination Namespace", f"(WORK-02) pe.{uuaa.lower()}.app-id-xxxx.dev"])
    t.add_row(["Destination Dataobject", f"x_{text_schema.lower()}_hdfs_{table_name2}_{schema_datax_version}"])
    t.add_row([f"", f""])
    t.add_row(["CONFIGURATION_INFO", f""])
    t.add_row(["-----------", f""])
    t.add_row([f"", f""])
    t.add_row([f"", f""])
    t.add_row([f"", f""])
    t.add_row(["METADATA_INFO", f""])
    t.add_row(["-------------", f""])
    t.add_row(["firstExecutionDate", f"{_frequency.upper()}"])
    t.add_row(["Periodicity", f"{_frequency.lower()}"])
    print(t)
